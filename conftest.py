import pytest
from playwright.sync_api import sync_playwright
from utils.config_reader import config
import allure


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        page = item.funcargs.get("page", None)

        if page:
            screenshot_path = f"reports/screenshots/{item.name}.png"
            page.screenshot(path=screenshot_path, full_page=True)

            allure.attach.file(
                screenshot_path,
                name="Screenshot",
                attachment_type=allure.attachment_type.PNG
            )

            # Attach DOM
            html = page.content()
            allure.attach(
                html,
                name="DOM Snapshot",
                attachment_type=allure.attachment_type.HTML
            )


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = getattr(p, config["browser"]).launch(
            headless=config["headless"]
        )

        context = browser.new_context()
        page = context.new_page()

        # ✅ Auto navigation (THIS is what you wanted)
        page.goto(config["base_url"])

        yield page

        context.close()
        browser.close()
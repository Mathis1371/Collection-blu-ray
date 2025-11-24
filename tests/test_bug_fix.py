
import os
import threading
import time
from http.server import SimpleHTTPRequestHandler, HTTPServer
from playwright.sync_api import sync_playwright

# Start a simple HTTP server in a separate thread
def start_server():
    server = HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
    server.serve_forever()

def test_actor_link_view_switching():
    # Start server
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    # Give it a moment to start
    time.sleep(1)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Load the served HTML file
            page.goto("http://localhost:8001/index.html")

            # Click on "Prochainement" tab to switch view
            page.click("#tabUpcoming")

            # Wait for movie "Le silence des agneaux"
            page.wait_for_selector("text=Le silence des agneaux", timeout=5000)

            # Click on the movie card to open modal
            page.click("text=Le silence des agneaux")

            # Wait for modal
            page.wait_for_selector("#modalContent")

            # Click on an actor (Jodie Foster)
            page.click("text=Jodie Foster")

            # Wait a bit for transitions
            page.wait_for_timeout(1000)

            # Check visibility of views
            grid_view = page.locator("#gridView")
            upcoming_view = page.locator("#upcomingView")

            # Grid view should be visible
            assert grid_view.is_visible(), "Grid View should be visible after clicking actor"

            # Upcoming view should be hidden
            assert not upcoming_view.is_visible(), "Upcoming View should be hidden after clicking actor"

            print("Test PASSED: View switching works correctly.")

        except Exception as e:
            print(f"Test FAILED: {e}")
            raise e
        finally:
            browser.close()

if __name__ == "__main__":
    test_actor_link_view_switching()

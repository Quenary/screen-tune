import requests
from packaging import version


def check_latest_release(repo_url: str, current_version: str) -> dict:
    """
    Get latest release info from GitHub
    """
    api_url = (
        repo_url.replace("https://github.com/", "https://api.github.com/repos/")
        + "/releases/latest"
    )
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        release_data = response.json()

        latest_version = release_data.get("tag_name", "")
        release_url = release_data.get("html_url", "")

        is_update_available = version.parse(latest_version) > version.parse(
            current_version
        )

        return {
            "latest_release_url": release_url,
            "update_available": is_update_available,
            "latest_version": latest_version,
        }

    except requests.RequestException as e:
        return {"error": f"Failed to fetch release info: {e}"}
    except Exception as e:
        return {"error": f"Unexpected error: {e}"}

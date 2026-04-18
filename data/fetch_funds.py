import requests
import json
import time

BASE_URL = "https://api.mfapi.in/mf"


# 🔥 Risk assignment logic
def assign_risk(category):
    if not category:
        return "Medium"

    category = category.lower()

    if "equity" in category:
        return "High"
    elif "debt" in category:
        return "Low"
    elif "hybrid" in category:
        return "Medium"
    else:
        return "Medium"


def fetch_funds(limit=30):
    try:
        print("🚀 Fetching list of funds...")
        response = requests.get(BASE_URL)
        response.raise_for_status()
        data = response.json()

        selected = data[:limit]
        result = []

        for fund in selected:
            code = fund.get("schemeCode")

            try:
                detail_url = f"{BASE_URL}/{code}"
                detail_response = requests.get(detail_url)
                detail_response.raise_for_status()
                detail = detail_response.json()

                meta = detail.get("meta", {})
                nav_data = detail.get("data", [])

                if not nav_data:
                    continue

                latest_nav = nav_data[0]

                fund_name = meta.get("scheme_name", "Unknown Fund")
                category = meta.get("scheme_category", "Unknown Category")
                amc = meta.get("fund_house", "Unknown AMC")
                nav = float(latest_nav.get("nav", 0))

                # ✅ Assign risk dynamically
                risk = assign_risk(category)

                # 🔥 Description for embeddings
                description = (
                    f"{fund_name} is a {category} mutual fund managed by {amc}. "
                    f"It has a {risk} risk level and latest NAV is {nav}."
                )

                result.append({
                    "fund_name": fund_name,
                    "category": category,
                    "amc": amc,
                    "nav": nav,
                    "risk": risk,
                    "description": description
                })

                print(f"✅ Processed: {fund_name} | Risk: {risk}")

                time.sleep(0.25)

            except Exception as e:
                print(f"⚠️ Skipping fund {code}: {e}")
                continue

        # Save JSON
        with open("data/sample_funds.json", "w") as f:
            json.dump(result, f, indent=2)

        print("\n🎉 Data fetched and saved to data/sample_funds.json")
        print(f"📊 Total funds saved: {len(result)}")

    except Exception as e:
        print(f"❌ Error fetching fund list: {e}")


if __name__ == "__main__":
    fetch_funds(limit=30)
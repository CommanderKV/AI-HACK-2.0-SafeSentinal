import csv
import requests
import concurrent.futures
from requests.adapters import HTTPAdapter


def fetch_website_content(url):
    def run(url):
        try:
            response = requests.get(url, timeout=3)
        except Exception as e:
            print("[ERROR]", e)
            return None
        
        if response.status_code == 200:
            return response.text
        else:
            return None
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future = executor.submit(run, url)
        try:
            result = future.result(timeout=3)
        except:
            print("[TIMEOUT] Failed to fetch", url, "within 3 seconds.")
            result = None

        return result

def classify_website(url, type_category):
    safeCategories = ["benign", "safe"]
    suspiciousCategories = ['defacement', "unsure"]
    unsafeCategories = ["malware", "phishing"]
    if type_category in safeCategories:
        return 0
    elif type_category in suspiciousCategories:
        return 1
    elif type_category in unsafeCategories:
        return 2
    else:
        print("UNKNOWN THREAT TYPE: ", type_category, "for URL: ", url, "Skipping...")
        return -1

def write_to_csv(data, filename):
    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['URL', 'Content', 'Threat'])
        for url, content, threat in data:
            try:
                writer.writerow([url, str(content), threat])
            except:
                print("Failed to write", url, "\n\n", content, "\n\n", threat, "to the dataset. Skipping...")

def process_csv(filename):
    website_content = []
    lines = [["url", "type"]]
    counter = 0

    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row
        for row in reader:
            lines.append(row)
            if (counter >= 200):
                break
            url = row[0]

            # Add missing elements of the URL
            if "www." not in url[:15] and "http" not in url[:15]:
                url = "www." + url

            if ("http" not in url):
                url = "https://" + url
            
            try:
                type_category = row[1]
            except:
                print("Failed to fetch type for", url, "|", row)
                type_category = "unsure"
            
            print("[CONNECTION] Fetching", url, "...")

            # Try to get the website content
            try:
                content = fetch_website_content(url)
            except:
                print("Failed to fetch", url, "with https. Trying http...")
                try:
                    url = url.replace("https", "http")
                    content = fetch_website_content(url)
                except:
                    print("Failed to fetch", url)
                    content = None

            # Classify the website
            threat = classify_website(url, type_category)
            if content and threat != -1:
                website_content.append((url, content, threat))
                print("[ADDED]", url, "to the dataset.")
                counter += 1
            
            else:
                print("[REMOVING]", url, "from the dataset.")
                with open("malicious_phish.csv", 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(lines)

                
    return website_content

def main():
    classified_websites = process_csv('malicious_phish.csv')
    if classified_websites:
        write_to_csv(classified_websites, 'classified_websites.csv')

if __name__ == '__main__':
    #print((fetch_website_content('https://www.google.com')))
    main()
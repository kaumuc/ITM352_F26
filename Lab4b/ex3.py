# Get a URL from the user, clean it, and extract the domain name and TLD (top-level domain)
# Name: Kaumualii Clemente
# Date: Sept. 18, 2026

url = input("Enter a URL: ")

cleaned_url = url.replace("http://", "")
cleaned_url = cleaned_url.replace("/", "")
print("Cleaned URL:", cleaned_url)

parts = cleaned_url.split(".") 
print("The parts are:", parts)

domain_name_ = parts[1]
TLD = parts[2]
print("The domain name is:", domain_name_)
print("The TLD is:", TLD)
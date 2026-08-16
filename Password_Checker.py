import requests
import hashlib
import sys
import getpass

def request_api_data(query_char):
    url = "https://api.pwnedpasswords.com/range/" + query_char

    response = requests.get(url)

    if response.status_code != 200:
        raise RuntimeError(
            f"Error fetching: {response.status_code}. Check the API and try again."
        )
    
    return response

def get_password_leaks_count(hashes, hash_to_check):
    for line in hashes.text.splitlines():
        h, count = line.split(":")
        if h == hash_to_check:
            return count

    return 0

def pwned_api_check(password):
    hashed = hashlib.sha1(password.encode()).hexdigest().upper()

    prefix = hashed[:5]
    suffix = hashed[5:]

    response = request_api_data(prefix)

    return get_password_leaks_count(response, suffix)

def main(args):
    for password in args:
        count = pwned_api_check(password)

        hidden_password = "*" * len(password)
        if count:
            print(
                f"{hidden_password} was found {count} times. "
                "You should probably change your password."
            )
        else:
            print(f"{hidden_password} was not found. Carry on!")

    return "Done!" 

if __name__ == "__main__":

    print("For multiple passwords, please add a space!")

    passwords = getpass.getpass("Enter your password/passwords: ").split()

    sys.exit(main(passwords))
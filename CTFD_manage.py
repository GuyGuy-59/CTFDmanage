import requests, json,urllib3, argparse, glob, random, string, csv, secrets
urllib3.disable_warnings()

#https://docs.ctfd.io/docs/api/redoc

def file_path(path):
    if glob.glob(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_file:{path} is not a valid path")

def generate_password(length):
    # Générer un mot de passe aléatoire avec des lettres majuscules, minuscules et des chiffres
    characters = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def Create_Users_password(fileCSV):
    with open(f'{fileCSV}') as csvfile:
        reader = csv.DictReader(csvfile,delimiter=',')
        rows = list(reader)
        for row in rows:
            if not row['password']:
                row['password'] = generate_password(10)

    with open(fileCSV, 'w', newline='') as csv_file:
            fieldnames = ['name', 'email', 'password']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)



def Create_Users(fileCSV):
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {token}"})
    # See users.csv example template at https://docs.ctfd.io/docs/imports/csv#users
    with open(f'{fileCSV}') as csvfile:
        users = csv.DictReader(csvfile, delimiter=',')
        for user in users:
            # Note that the notify parameter is being passed here so CTFd will send the 
            # user an email with their credentials after the account is created
            r = s.post(
                f"{url}/api/v1/users?notify=true",
                json={
                    "name": user["name"],
                    "email": user["email"],
                    "password": user["password"],
                    "type": "user",
                    "verified": True,
                    "hidden": False,
                    "banned": False,
                    "fields": [],
                },
                headers={"Content-Type": "application/json"},
                verify=False
            )
            if r.status_code == 200:
                print(json.dumps(r.json(), indent=4))
            else:
                print(r.text)

def Get_Users():
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {token}"})
    r = s.get(f"{url}/api/v1/users",headers={"Content-Type": "application/json"},verify=False)
    if r.status_code == 200:
        print(json.dumps(r.json(), indent=4))
    else:
        print(r.text)

def Delete_Users(fileCSV):
    s = requests.Session()
    s.headers.update({"Authorization": f"Token {token}"})
    # See users.csv example template at https://docs.ctfd.io/docs/imports/csv#users
    with open(f'{fileCSV}') as csvfile:
        users = DictReader(csvfile,delimiter=',')
        for user in users:
            # NOTE: It is important below to set the json argument so that requests sets the Content-Type correctly.
            r = s.delete(f"{url}/api/v1/users/{user['id']}", json="",verify=False)
            if r.status_code == 200:
               print(json.dumps(r.json(), indent=4))
            else:
                print(r.text)


if __name__ == "__main__":
    module_functions = {
    'CreateUsers': Create_Users,
    'GetUsers': Get_Users,
    'DeleteUsers':Delete_Users
    }

    parser = argparse.ArgumentParser(add_help=True)
    parser.add_argument('-t', '--target', help='Target IP:PORT or Domain:PORT CTFD', type=str,required=True)
    parser.add_argument('--token', help='https://docs.ctfd.io/docs/api/getting-started#api-endpoint-documentation', type=str,required=True)
    parser.add_argument('-M', '--module',  choices=module_functions.keys(), help='Specify the module to execute')
    parser.add_argument('--path', type=file_path, help='Specify the valid path')
    #parser.add_argument('-d', '--data', nargs='+',type=dir_path, help='Additional data to pass to the specified module.')
    args= parser.parse_args()
    url=f'https://{args.target}'
    token =f'{args.token}'
    module = args.module
    selected_function = module_functions.get(module, None)
    if args.path:
        selected_function(args.path)
    else:
        print(selected_function())


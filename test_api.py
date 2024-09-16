import os
from dotenv import load_dotenv
from github import Github
from github import Auth

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    what = load_dotenv(dotenv_path)

access_token = os.getenv("API_TOKEN")
repo_name = os.getenv("REPO_NAME")
user_name = os.getenv("USER_NAME")
auth = Auth.Token(access_token)

g = Github(auth=auth)

while True:
    user = g.get_user()
    user_reps = user.get_repos()
    error_input_flag = False
    action_number = input("\nВыберите действие:\n"
                          "1 - Создать новый репозиторий\n"
                          "2 - Посмотреть названия всех текущих репозиториев и их количество\n"
                          "3 - Удалить существующий репозиторий\n"
                          "4 - Выход\n")
    try:
        action_number = int(action_number)
    except:
        error_input_flag = True
    if action_number not in (1, 2, 3, 4):
        error_input_flag = True
    if error_input_flag:
        print("Вы ввели что-то отличное от цифр 1,2,3,4")
        continue

    if action_number == 1:
        created_flag = False
        print('Для данного теста предусмотрено создание репозитория с конкретным названием из .env')
        for rep in user_reps:
            if rep.name == repo_name:
                created_flag = True
                print("Тестовый репозиторий с таким названием уже был создан, сначала удалите его если хотите создать снова")
                continue
        if not created_flag:
            example_repo = user.create_repo(repo_name)
            print(f'Репозиторий с названием "{example_repo.name}" был успешно создан')

    if action_number == 2:
        print(f'Общее количество репозиториев - {user_reps.totalCount}')
        for rep in user_reps:
            rep_name = rep.name
            print(rep_name)

    if action_number == 3:
        deleted_flag = False
        for rep in user_reps:
            if rep.name == repo_name:
                rep.delete()
                print(f'Тестовый репозиторий с названием "{rep.name}" был успешно удалён')
                deleted_flag = True
                continue
        if not deleted_flag:
            print(f"Тестовый репозиторий с названием '{repo_name}' ещё не был создан, потому не может быть удалён")

    if action_number == 4:
        g.close()
        break

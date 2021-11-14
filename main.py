import vk_api
import re
import time

session = vk_api.VkApi(token="37f1bb91fe2ea79a7d1c47962f38b8d1e8fc895c2d73f2e233c4d71b3e80045b5f1d7d6e27e8f975a7902")
vk = session.get_api()

start_time = time.time()
# построчно собирает ссылки в список
names = []
while True:
    name = str(input())
    if name:
        names.append(name)
    else:
        break

# собирает ID у всех людей в списке
pattern = r"https://vk.com/"
id_list = []
for link in names:
    n = re.sub(pattern, "", link)
    if re.search(r"id\d+", n):
        id_list.append(re.sub("id", "", n))
    else:
        user_name = session.method("users.get", {"user_ids": n, "fields": "id"})
        id_list.append(user_name[0]["id"])

friends_list = []
# берет список друзей у каждого человека и заносит его в общий список
for id in id_list:
    friend = session.method("friends.get", {"user_id": id})
    friends_list.append(friend["items"])


def get_user_friends(list):
    for friends in list[0]:     # перебор друзей первого человека
        flag = False
        for people in range(len(list)):
            if friends not in list[people]:
                flag = True
        if not flag:
            # берет у каждого человека ID его аватарки
            user_name = session.method("users.get", {"user_ids": friends, "fields": "photo_id"})
            key = "photo_id"
            # проверяет есть у человека стоит фотография на аватарке
            photo = None
            if key in user_name[0]:
                photo = ("https://vk.com/id" + str(user_name[0]["id"]) + "?z=photo" + str(photo) + "%2Falbum141937306_0%2Frev")

            print("https://vk.com/id" + str(user_name[0]["id"]), user_name[0]["last_name"], user_name[0]["first_name"],
                  photo)


get_user_friends(friends_list)
print("--- %s seconds ---" % (time.time() - start_time))
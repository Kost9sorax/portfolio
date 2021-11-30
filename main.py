import vk_api
import re
import time

session = vk_api.VkApi(token="")
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
userids = []
for link in names:
    n = re.sub(pattern, "", link)
    if re.search(r"id\d+", n):
        userids.append(re.sub("id", "", n))
    else:
        user_name = session.method("users.get", {"user_ids": n, "fields": "id"})
        userids.append(user_name[0]["id"])

friends = []
# берет список друзей у каждого человека и заносит его в общий список
for id in userids:
    friend = session.method("friends.get", {"user_id": id})
    friends.append(friend["items"])


def get_user_friends(friends_with_friends):
    for friend in friends_with_friends[0]:     # перебор друзей первого человека
        flag = False
        for people in friends_with_friends:    # проверка на то есть ли друг первого человека у всех остальных
            if friend not in people:
                flag = True     # если хотя бы у одного его в друзьях нет то алгоритм дальше не идет
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


get_user_friends(friends)
print("--- %s seconds ---" % (time.time() - start_time))

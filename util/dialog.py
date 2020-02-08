from pg.pginstance import PgInstance


def get_checklist(db):
    checklist = db.Get_checklist()
    leetcode_username_emoji = "❎"
    daily_goal_emoji = "❎"
    reminder_time_emoji = "❎"
    if checklist["leetcode_username"] != None:
        leetcode_username_emoji = "✅"
    if checklist["daily_goal"] != None:
        daily_goal_emoji = "✅"
    if checklist["reminder_time"] != None:
        reminder_time_emoji = "✅"
    checklist_msg = (
        "1.  Your LeetCode username "
        + leetcode_username_emoji
        + "\n2. A daily goal for the number of questions completed "
        + daily_goal_emoji
        + "\n3. The time of day to remind you "
        + reminder_time_emoji
    )
    return checklist_msg

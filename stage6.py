from datetime import datetime

notifications = [
    {
        "ID": "1",
        "Type": "Placement",
        "Message": "Microsoft Hiring",
        "Timestamp": "2026-06-18 10:00:00"
    },
    {
        "ID": "2",
        "Type": "Result",
        "Message": "Mid Sem Result",
        "Timestamp": "2026-06-18 09:00:00"
    },
    {
        "ID": "3",
        "Type": "Event",
        "Message": "Tech Fest",
        "Timestamp": "2026-06-18 08:00:00"
    }
]

weights = {
    "Placement": 3,
    "Result": 2,
    "Event": 1
}

now = datetime.now()

for n in notifications:
    timestamp = datetime.strptime(
        n["Timestamp"],
        "%Y-%m-%d %H:%M:%S"
    )

    age_hours = max(
        (now - timestamp).total_seconds() / 3600,
        1
    )

    n["priority"] = weights[n["Type"]] * (1 / age_hours)

top_notifications = sorted(
    notifications,
    key=lambda x: x["priority"],
    reverse=True
)

print("\nTOP PRIORITY NOTIFICATIONS\n")

for item in top_notifications[:10]:
    print(
        f"{item['Type']} | "
        f"{item['Message']} | "
        f"Priority: {item['priority']:.4f}"
    )
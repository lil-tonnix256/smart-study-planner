# Smart Study Planner
# Individual Assignment
# A console-based Python program for recording and analysing study sessions.

FILE_NAME = "study_log.txt"


def classify_session(duration):
    """
    Classifies a study session based on its duration.
    Under 30 minutes = Short
    30 to 90 minutes = Medium
    Over 90 minutes = Long
    """
    if duration < 30:
        return "Short"
    elif duration <= 90:
        return "Medium"
    else:
        return "Long"


def add_session(sessions):
    """
    Prompts the user for study session details and adds
    the session to the sessions list.
    """
    print("\n--- Add Study Session ---")

    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day label: ").strip()

    # Keep asking until the user enters a positive number.
    while True:
        try:
            duration = float(input("Enter duration in minutes: "))

            if duration > 0:
                break
            else:
                print("Duration must be a positive number.")

        except ValueError:
            print("Invalid input. Please enter a number.")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    sessions.append(session)

    print("Study session added successfully!")


def view_sessions(sessions):
    """
    Displays all study sessions in a formatted table.
    """
    print("\n--- All Study Sessions ---")

    if not sessions:
        print("No study sessions have been recorded.")
        return

    print("-" * 90)
    print(f"{'No.':<5}{'Subject':<20}{'Topic':<25}"
          f"{'Date':<15}{'Duration':<12}{'Class':<10}")
    print("-" * 90)

    for index, session in enumerate(sessions, start=1):
        classification = classify_session(session["duration"])

        print(
            f"{index:<5}"
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12.1f}"
            f"{classification:<10}"
        )

    print("-" * 90)


def search_by_subject(sessions):
    """
    Searches for study sessions by subject.
    The search is not case-sensitive.
    """
    print("\n--- Search Sessions by Subject ---")

    subject = input("Enter subject to search: ").strip()

    # Convert both values to lowercase so that the search
    # is not affected by capitalization.
    matching_sessions = [
        session for session in sessions
        if session["subject"].lower() == subject.lower()
    ]

    if not matching_sessions:
        print(f"No study sessions found for '{subject}'.")
        return

    total_time = sum(
        session["duration"] for session in matching_sessions
    )

    print(f"\nSessions for subject: {subject}")
    print("-" * 85)
    print(f"{'No.':<5}{'Topic':<25}{'Date':<15}"
          f"{'Duration':<15}{'Class':<15}")
    print("-" * 85)

    for index, session in enumerate(matching_sessions, start=1):
        classification = classify_session(session["duration"])

        print(
            f"{index:<5}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<15.1f}"
            f"{classification:<15}"
        )

    print("-" * 85)
    print(f"Total time spent on {subject}: {total_time:.1f} minutes")
    print(f"Total time in hours: {total_time / 60:.2f} hours")


def study_statistics(sessions):
    """
    Calculates and displays study statistics:
    - Total hours studied
    - Total hours per subject
    - Subject with least study time
    - Longest individual study session
    """
    print("\n--- Study Statistics ---")

    if not sessions:
        print("No study sessions available for statistics.")
        return

    # Calculate total study time in minutes.
    total_minutes = sum(
        session["duration"] for session in sessions
    )

    print(f"\nTotal hours studied overall: {total_minutes / 60:.2f} hours")

    # Dictionary used to store total study time for each subject.
    subject_totals = {}

    for session in sessions:
        subject = session["subject"]

        if subject in subject_totals:
            subject_totals[subject] += session["duration"]
        else:
            subject_totals[subject] = session["duration"]

    print("\nTotal hours studied per subject:")

    for subject, minutes in subject_totals.items():
        print(f"- {subject}: {minutes / 60:.2f} hours")

    # Find the subject with the smallest total study time.
    weakest_subject = min(
        subject_totals,
        key=subject_totals.get
    )

    print(
        f"\nSubject with the least study time: "
        f"{weakest_subject} "
        f"({subject_totals[weakest_subject] / 60:.2f} hours)"
    )

    # Find the longest individual study session.
    longest_session = max(
        sessions,
        key=lambda session: session["duration"]
    )

    print("\nLongest study session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Date: {longest_session['date']}")
    print(f"Duration: {longest_session['duration']:.1f} minutes")
    print(
        f"Classification: "
        f"{classify_session(longest_session['duration'])}"
    )


def save_sessions(sessions):
    """
    Saves all study sessions to study_log.txt.
    Each session is stored on one line using | as a separator.
    """
    try:
        with open(FILE_NAME, "w") as file:

            for session in sessions:
                file.write(
                    f"{session['subject']}|"
                    f"{session['topic']}|"
                    f"{session['date']}|"
                    f"{session['duration']}\n"
                )

        print("Study sessions saved successfully.")

    except OSError as error:
        print(f"Error saving sessions: {error}")


def load_sessions():
    """
    Loads previously saved sessions from study_log.txt.
    If the file does not exist, an empty list is returned.
    """
    sessions = []

    try:
        with open(FILE_NAME, "r") as file:

            for line in file:
                line = line.strip()

                if not line:
                    continue

                parts = line.split("|")

                # Make sure the saved record has all four fields.
                if len(parts) == 4:
                    subject, topic, date, duration = parts

                    try:
                        session = {
                            "subject": subject,
                            "topic": topic,
                            "date": date,
                            "duration": float(duration)
                        }

                        sessions.append(session)

                    except ValueError:
                        print("Warning: A saved record was invalid and skipped.")

    except FileNotFoundError:
        # This is normal on the first run of the program.
        print("No previous study log found. Starting with an empty record.")

    except OSError as error:
        print(f"Error loading study sessions: {error}")

    return sessions


def display_menu():
    """
    Displays the main menu.
    """
    print("\n" + "=" * 50)
    print("           SMART STUDY PLANNER")
    print("=" * 50)
    print("1. Add a study session")
    print("2. View all sessions")
    print("3. Search sessions by subject")
    print("4. View statistics")
    print("5. Save and exit")
    print("=" * 50)


def main():
    """
    Main function controlling the Smart Study Planner.
    """
    # Automatically load previously saved sessions.
    sessions = load_sessions()

    while True:
        display_menu()

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)

        elif choice == "2":
            view_sessions(sessions)

        elif choice == "3":
            search_by_subject(sessions)

        elif choice == "4":
            study_statistics(sessions)

        elif choice == "5":
            save_sessions(sessions)
            print("Thank you for using Smart Study Planner!")
            break

        else:
            print("Invalid choice. Please select a number from 1 to 5.")


# Program entry point
if __name__ == "__main__":
    main()
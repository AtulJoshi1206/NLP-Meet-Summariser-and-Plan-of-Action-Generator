import openai
import os

# Set the OpenAI API key
openai_api_key = ""

def generate_plan_of_action(transcript):
    """
    Generates a plan of action based on the given transcript.

    :param transcript: The transcript text
    :return: Generated plan of action text
    """
    prompt = (
        "Based on the following meeting transcript, generate a detailed plan of action with at least five actionable points:\n\n"
        f"{transcript}\n\n"
        "Plan of Action:\n1."
    )

    client = openai.Client(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500,
        temperature=0.7,
    )
    plan_of_action = response.choices[0].message.content.strip()
    return plan_of_action


def save_plan_of_action(transcript_path, plan_of_action_path):
    """
    Generates a plan of action from a transcript and saves it to a text file.

    :param transcript_path: Path to the transcript file
    :param plan_of_action_path: Path to save the plan of action
    :return: None
    """
    with open(transcript_path, 'r', encoding='utf-8') as file:
        transcript = file.read()

    plan_of_action = generate_plan_of_action(transcript)

    with open(plan_of_action_path, 'w', encoding='utf-8') as file:
        file.write(plan_of_action)

    print(f"Plan of action saved to {plan_of_action_path}.")


# Example usage with user input
if __name__ == "__main__":
    transcript_path = input("Enter the path of the transcript file: ")
    plan_of_action_path = input("Enter the path to save the plan of action file: ")
    save_plan_of_action(transcript_path, plan_of_action_path)

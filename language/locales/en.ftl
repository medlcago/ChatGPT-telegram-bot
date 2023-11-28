debug-message =
    Technical work is underway.
    The bot is temporarily unavailable.

blocked-message =
    <b>Access is denied.
    Most likely, you have been banned for violating the rules of the bot.</b>

subscribers-only-message = <b>To use the bot, you must purchase a subscription.</b>

start-message =
    Hello, {$full_name}!

    This bot gives you access to ChatGPT and Dall-E to create text and images.

    Bot uses gpt-3.5-turbo/gpt-4 models

    Chatbot can:
    1. Create images
    2. Write and edit texts
    3. Translate from any language to any
    4. Write and edit code
    5. Answer questions
    6. Make summaries from YouTube videos

    You can communicate with the bot, as with a live interlocutor, asking questions in any language. Please note that sometimes the bot makes up facts and also has limited knowledge of events after 2021.

    ✉️ To get a text answer, just write your question in the chat.

    🌅 To create an image, start a request with the /image command and then add a description.

    🎬 To make a summary of a YouTube video, use the /summary command, followed by a link to the video separated by a space.

sub-start-message =
    Current model: {$current_model}
    Send a message to start a dialog

    /clear - Clear dialog history
    /switch - Change model
    /models - List of available models

help-message =
    <b>📝 Text generation</b>
    To generate texts using GPT, just write a request in the chat. The default model is gpt-3.5-turbo. Users with a subscription can change models using the <b>/switch</b> command

    🎬 Creating a summary from YouTube video
    <b>/summary and link to video</b> - The bot analyzes the video and provides a text summary

    🌅 Image generation
    <b>/image and short description</b> - Image generation

    <b>⚙️ Other bot commands</b>
    <b>/clear</b> - Start a new dialogue without taking into account the context (By default, the bot remembers the context)
    <b>/switch</b> - Change model (Temporarily available to all)
    <b>/models</b> - List of models available for work

my-profile-message =
    👤 Your profile
    ├ ID: <code>{$user_id}</code>
    ├ Subscription: <code>{$status}</code>
    ├ Number of referrals: <code>{$referral_count}</code>
    └ Current model: <code>{$current_model}</code>

processing-request-message = Processing request, please, wait

model-selection-message = Select a model below 👇

cancel-message = The action has been canceled.

switch-chat-type-message =
    Current model: <b><i>{$current_model}</i></b>

    The message history has been cleared.

clear-dialog-history-message = The message history has been cleared.

non-premium-message = The command <b><i>{$command}</i></b> is only available to premium users.

model-not-found = Error: Model <b><i>{$model}</i></b> not found

empty-command-message = The command <b><i>{$command}</i></b> was empty, the request could not be completed."

non-text-message = The bot can only work with text. Please, repeat your request in text form.

contact-admin-message =
    Contact the administrator.

    Enter your message and wait for a response from the administrator.

    You can cancel this action with the command <b><i>/cancel</i></b>

    <b>A response will be received within <i>24 hours</i></b>

    ❗If you delete your message, there will be no response to it.

message-to-administrator-message =
    Your message:
    {$message}

    The administrator will answer you within <b><i>24 hours</i></b>

debug-message =
    Ведутся технические работы.
    Бот временно недоступен.

blocked-message =
    <b>Access denied.
    The request has not been fulfilled.</b>

subscribers-only-message = <b>Для использования бота необходимо приобрести подписку.</b>

start-message =
    Привет, {$full_name}!

    Этот бот открывает вам доступ к ChatGPT и Dall-E для создания текста и изображений.

    Бот использует модели gpt-3.5-turbo/gpt-4

    Чатбот умеет:
    1. Создавать изображения
    2. Писать и редактировать тексты
    3. Переводить с любого языка на любой
    4. Писать и редактировать код
    5. Отвечать на вопросы
    6. Делать саммари из YouTube-видео

    Вы можете общаться с ботом, как с живым собеседником, задавая вопросы на любом языке. Обратите внимание, что иногда бот придумывает факты, а также обладает ограниченными знаниями о событиях после 2021 года.

    ✉️ Чтобы получить текстовый ответ, просто напишите в чат ваш вопрос.

    🌅 Чтобы создать изображение, начните запрос с команды /image, а затем добавьте описание.

    🎬 Чтобы сделать саммари из YouTube-видео, используйте команду /summary, а затем через пробел ссылку на видео.

sub-start-message =
    Текущая модель: {$current_model}
    Отправьте сообщение, чтобы начать диалог

    /clear - Очистить историю диалога
    /switch - Сменить модель
    /models - Список доступных моделей

help-message =
    <b>📝 Генерация текстов</b>
    Для генерации текстов при помощи GPT проcто напишите запрос в чат. По умолчанию используется модель gpt-3.5-turbo. Пользователи с подпиской могут менять модели командой <b>/switch</b>

    🎬 Создание саммари из YouTube-видео
    <b>/summary и ссылка на видео</b> - Бот анализирует видео и выдает текстовое саммари

    🌅 Генерация изображений
    <b>/image и краткое описание</b> - Генерация изображения

    <b>⚙️ Другие команды бота</b>
    <b>/clear</b> - Начать новый диалог без учета контекста (По умолчанию бот запоминает контекст)
    <b>/switch</b> - Сменить модель (Временно доступно всем)
    <b>/models</b> - Список доступных для работы моделей

my-profile-message =
    👤 Ваш профиль
    ├ ID: <code>{$user_id}</code>
    ├ Подписка: <code>{$status}</code>
    ├ Кол-во рефералов: <code>{$referral_count}</code>
    └ Текущая модель: <code>{$current_model}</code>

processing-request-message = Обработка запроса, ожидайте

model-selection-message = Выберите модель ниже 👇

cancel-message = Действие было отменено.

switch-chat-type-message =
    Текущая модель: <b><i>{$current_model}</i></b>

    История сообщений была очищена.

clear-dialog-history-message = История сообщений была очищена.

non-premium-message = Команда <b><i>{$command}</i></b> доступна только premium пользователям.

model-not-found = Ошибка: модель <b><i>{$model}</i></b> не найдена

empty-command-message = Команда <b><i>{$command}</i></b> оказалась пустой, запрос не может быть выполнен.

non-text-message = Бот умеет работать только с текстом. Пожалуйста, повторите свой запрос в текстовом виде.

contact-admin-message =
    Связь с администратором.

    Введите ваше сообщение и ожидайте ответа от администратора.

    Вы можете отменить это действие командой <b><i>/cancel</i></b>

    <b>Ответ поступит в течение <i>24 часов</i></b>

    ❗Если вы удалите свое сообщение, то ответа на него не последует.

message-to-administrator-message =
    Ваше сообщение:
    {$message}

    Администратор ответит вам в течение <b><i>24 часов</i></b>
import os
import gradio as gr
from litellm import completion

# встановлюємо змінну середовища для COHERE_API_KEY; мій trial ключ
os.environ["COHERE_API_KEY"] = 'AbTU8gQ2cjzBDseA5SB6umXMGFFH3azjKQBQ6iq3'


# Функція для отримання відповіді від Cohere
def get_cohere_response(user_input):

    # перевіримо довжину запиту
    if len(user_input) < 5:
        return "Схоже, щось пішло не так. Спробуй перефразувати своє питання у форматі '*поняття* це?' " \
               "або 'що таке *поняття*?' та надішли запит ще раз.\n Looks like something went wrong. Use the " \
               "formulation '*concept* is?' or 'what is *concept*?' and try again."

    # вказівка щодо формату відповіді
    prompt = f"Explain the question in simple words. Give some analogy from real life. " \
             f"If the text is not in English, write the answer using language of the question. " \
             f"Question: {user_input}"

    response = completion(
        model="command-r",  # Модель "command-r"
        messages=[{
            "content": prompt,
            "role": "user"
        }]
    )
    return response.choices[0].message.content  # лише відповідь-текст


# Створюємо інтерфейс Gradio
def interface():
    with gr.Blocks() as iface:
        gr.Markdown("### Простими словами")
        gr.Markdown("Заплутали хитромудрі терміни й голова кипить від усіх тих карколомних понять? Чимдуж хапайтесь за"
                    " можливість нарешті розшифрувати їх на просту й доступну мову, доповнену аналогіями із реального "
                    "життя. Просто введіть запит, натисніть кнопку — і отримаєте відповідь! "
                    "<br> _*З використанням моделі [Cohere Command-R](https://cohere.com)._")
        # Вхідне текстове поле
        user_input = gr.Textbox(label="Введіть запит", placeholder="Що таке квантова механіка?")

        # Виведення відповіді
        output = gr.Textbox(label="Відповідь", interactive=False)

        # Кнопка для відправки запиту
        submit_btn = gr.Button("Отримати відповідь")

        # Визначення дії при натисканні кнопки
        submit_btn.click(get_cohere_response, inputs=user_input, outputs=output)

    iface.launch()


interface()  # виклик інтерфейсу

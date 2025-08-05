#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!pip install openai


# In[1]:


import os
from openai import OpenAI


# In[2]:


api_key = os.getenv("OPENAI_API_KEY")


# In[ ]:


client = OpenAI(api_key=api_key)


# In[4]:


system_prompt = """ You are an assistant working for a telecommunications company. 
Your job is to help employees handle incoming customer emails quickly and professionally.

Follow these rules:
- Keep your tone professional, polite, and neutral.
- Never say anything negative about the company or its services.
- Avoid making promises you can’t verify.
- Be concise and clear.
- Do not engage with messages unrelated to the company’s services (e.g., spam, personal topics, or irrelevant requests). Instead, state clearly that the message is not relevant.
- If the issue should go to a specific department, say you will forward the email.
- When appropriate, include common troubleshooting steps in your response.

Return the following structured format:

- Category: [billing / technical / complaint / other]  

- Summary: [short 1-2 sentence summary of the customer’s email]  

- Proposed Response: [a brief, polite, and ready-to-send reply to the customer]

Common troubleshooting instructions (use when appropriate):
- For router not working: "Please try unplugging your router for 30 seconds, then plug it back in. If the issue continues, we’ll arrange a replacement."
- For slow internet: "Please restart your modem and check for background applications using bandwidth. Let us know if the issue continues."
- For invoice disputes: "Please review your account in the customer portal. We will also forward your message to the billing department."
- For SIM card not working: "Please try reinserting the SIM card and restarting your device. If the issue continues, we’ll arrange a replacement or further diagnostics."
- For call issues: "Please check if airplane mode is turned off and your device is connected to the network. If the issue persists, we will forward your case to our technical team."
"""


# In[5]:


departments = {
    "billing": "billing@company.com",
    "technical": "techsupport@company.com",
    "complaint": "customer-care@company.com"
}


# In[6]:


def detect_department(reply_text):
    lower = reply_text.lower()
    for key in departments:
        if key in lower:
            return key.capitalize(), departments[key]
    return None, None


# In[7]:


import ipywidgets as widgets
from IPython.display import display, clear_output

email_input = widgets.Textarea(
    placeholder='Paste customer email here...',
    description='Email:',
    layout=widgets.Layout(width='100%', height='150px')
)

submit_button = widgets.Button(description='Process Email', button_style='primary')
output_box = widgets.Output()


# In[8]:


def process_email(b):
    output_box.clear_output()
    user_email = email_input.value.strip()

    if not user_email:
        with output_box:
            print(" Please enter an email before clicking.")
        return

    user_query = f"Email:\n{user_email}"

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]

    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.4
        )

        assistant_reply = response.choices[0].message.content

        category, forward_email = detect_department(assistant_reply)

        with output_box:
            print("Assistant Output:\n")
            print(assistant_reply)
            if forward_email:
                print(f"\n📨 Suggested Forwarding: {category.capitalize()} Department – {forward_email}")

    except Exception as e:
        with output_box:
            print("Error:", str(e))


# In[9]:


submit_button.on_click(process_email)

display(email_input, submit_button, output_box)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





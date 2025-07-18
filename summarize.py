import requests

def summarize_text(text, model="llama3.2"):
    prompt = f"""Summarize the following text in less than 150 words
    such that all the key points are covered:\n\n{text}"""

    response = requests.post("http://localhost:11434/api/generate", json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })

    print("Status code:", response.status_code)
    print("Raw response text:", response.text)

    return response.json()["response"].strip()


# if __name__ == "__main__":
#     summary = summarize("""India, officially the Republic of India,[j][20] is a country in South Asia. It is the seventh-largest country by area; the most populous country since 2023;[21] and, since its independence in 1947, the world's most populous democracy.[22][23][24] Bounded by the Indian Ocean on the south, the Arabian Sea on the southwest, and the Bay of Bengal on the southeast, it shares land borders with Pakistan to the west;[k] China, Nepal, and Bhutan to the north; and Bangladesh and Myanmar to the east. In the Indian Ocean, India is near Sri Lanka and the Maldives; its Andaman and Nicobar Islands share a maritime border with Thailand, Myanmar, and Indonesia.

# Modern humans arrived on the Indian subcontinent from Africa no later than 55,000 years ago.[26][27][28] Their long occupation, predominantly in isolation as hunter-gatherers, has made the region highly diverse.[29] Settled life emerged on the subcontinent in the western margins of the Indus river basin 9,000 years ago, evolving gradually into the Indus Valley Civilisation of the third millennium BCE.[30] By 1200 BCE, an archaic form of Sanskrit, an Indo-European language, had diffused into India from the northwest.[31][32] Its hymns recorded the early dawnings of Hinduism in India.[33] India's pre-existing Dravidian languages were supplanted in the northern regions.[34] By 400 BCE, caste had emerged within Hinduism,[35] and Buddhism and Jainism had arisen, proclaiming social orders unlinked to heredity.[36] Early political consolidations gave rise to the loose-knit Maurya and Gupta Empires.[37] Widespread creativity suffused this era,[38] but the status of women declined,[39] and untouchability became an organized belief.[l][40] In South India, the Middle kingdoms exported Dravidian language scripts and religious cultures to the kingdoms of Southeast Asia.[41]

# In the early medieval era, Christianity, Islam, Judaism, and Zoroastrianism became established on India's southern and western coasts.[42] Muslim armies from Central Asia intermittently overran India's northern plains in the second millennium.[43] The resulting Delhi Sultanate drew northern India into the cosmopolitan networks of medieval Islam.[44] In south India, the Vijayanagara Empire created a long-lasting composite Hindu culture.[45] In the Punjab, Sikhism emerged, rejecting institutionalised religion.[46] The Mughal Empire ushered in two centuries of economic expansion and relative peace,[47] leaving a rich architectural legacy.[48][49] Gradually expanding rule of the British East India Company turned India into a colonial economy but consolidated its sovereignty.[50] British Crown rule began in 1858. The rights promised to Indians were granted slowly,
# """)
#     print("Summary:", summary)

def data_edit(trans, text):
    main_text = ''
    count = 0
    if len(text) > 500:
        while True:
            if len(text[count:]) >= 500:
                main_text += trans.translate(text[count:count + 500])
                count += 500
            else:
                main_text += trans.translate(text[count:])
                break
    else:
        main_text += trans.translate(text)
    if "&#39;" in main_text:  # noqa
        main_text = main_text.replace("&#39;", "'")
    if "&#10;" in main_text:
        main_text = main_text.replace("&#10;", '\n')
    if "&quot;" in main_text:
        main_text = main_text.replace("&quot;", '\"')
    if "&gt;" in main_text:
        main_text = main_text.replace("&gt;", '>')
    if "&lt;" in main_text:
        main_text = main_text.replace("&lt;", '<')
    return main_text


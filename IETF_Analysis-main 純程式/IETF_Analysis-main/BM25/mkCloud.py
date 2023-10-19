def mkCloud(txt):
    import numpy as np
    import matplotlib.pyplot as plt
    from wordcloud import WordCloud
    from PIL import Image
    mask = np.array(Image.open('BM25/alice_mask.png'))
    font = 'BM25/SourceHanSansTW-Regular.otf'
    # mask=mask,
    cloud = WordCloud(background_color='white', mask=mask, font_path=font,
                      contour_width=3, contour_color='steelblue').generate(txt)

    plt.imshow(cloud)
    plt.axis("off")
    # plt.show()
    # keywords 已經完成排序的 一個 dict
    keywords = cloud.words_
    mostly = list(keywords.keys())
    print('Top10 keywords: ', mostly[:10])
    """
    mostkeys = str(mostly[:10])
    pmt = f'Top10 keywords in the text\n{mostkeys}'
    print(pmt)
    """
    # 將wordcloud 存檔
    destFile = 'BM25/bmFig.jpg'
    cloud.to_file(destFile)

    # show image on screen
    '''''
    if os.path.exists(destFile):
        img = Image.open(destFile, 'r')
        img.show()
    '''''

#!/usr/bin/python3
from bs4 import BeautifulSoup
import requests
import xlsxwriter

titleList = []
priceList = []
descriptionList = []
htmlText = []
header = ["Titre", "Prix", "Description"]
linkArticleList = []
imageLinkList = []

marque = "porsche"
model = input("Choissisez le modèle à rechercher : ")
firstRegistration = int(input("Choissisez l'année de parution : "))
country = input("Quel pays voulez-vous rechercher ? Belgique(B), Luxembourg(L), Allemagne(D), Pays-Bas(NL) : ")
numberOfPage = int(input("Combien de page voulez-vous regarder (0 si tout) : "))


def parser():
    n = 0
    k = 0
    i = 1

    if numberOfPage < 2 and numberOfPage != 0:
        htmlText.append(requests.get(f"https://www.autoscout24.com/lst/{marque}/{model}?sort=standard&desc=0&ustate=N,U&atype=C&fregfrom={firstRegistration}&cy={country}&page={numberOfPage}",  timeout=5).text)
    else:
        while i <= numberOfPage:
            htmlText.append(requests.get(f"https://www.autoscout24.com/lst/{marque}/{model}?sort=standard&desc=0&ustate=N,U&atype=C&fregfrom={firstRegistration}&cy={country}&page={i}",  timeout=5).text)
            i += 1

    while n < numberOfPage:
        soup = BeautifulSoup(htmlText[n], "lxml")
        articleTitle = soup.find_all("div", class_="ListItem_header__uPzec")
        linkEl = soup.find_all("a", class_="ListItem_title__znV2I Link_link__pjU1l")
        articleDescription = soup.find_all("div", class_="ListItem_listing__VjI4F")
        imageLink = soup.find_all("img", class_="NewGallery_img__bi92g")

        for el in articleTitle:
            title = el.find("a").text
            titleList.append(title)

        for el in articleDescription:
            price = " ||| " + el.find("p").text + " ||| "
            priceList.append(price)
            descriptionTags = el.find("div", class_="VehicleDetailTable_container__mUUbY").text
            descriptionList.append(descriptionTags)

        for el in linkEl:
            link = "https://www.autoscout24.com" + el.get("href")
            linkArticleList.append(link)

        for el in imageLink:
            image = el.get("src")
            imageLinkList.append(image)
            print(image)

        outWorkBook = xlsxwriter.Workbook("/home/eflay/Documents/CSV/test.xlsx")
        outSheet = outWorkBook.add_worksheet("Porsche")

        outSheet.write("A1", "Titre")
        outSheet.write("B1", "Prix")
        outSheet.write("C1", "Description")
        outSheet.write("D1", "Lien")
        #outSheet.write("E1", "Image")

        t = 2
        y = 22

        while k < len(titleList):
            if n > 0:
                for row_num, data in enumerate(titleList):
                    outSheet.write(row_num + 1, 0, data)
                for row_num, data in enumerate(priceList):
                    outSheet.write(row_num + 1, 1, data)
                for row_num, data in enumerate(descriptionList):
                    outSheet.write(row_num + 1, 2, data)
                for row_num, data in enumerate(linkArticleList):
                    outSheet.write_string(row_num + 1, 3, data)
                #for row_num, data in enumerate(imageLinkList):
                    #imageData = BytesIO(urlopen(data).read())
                    #outSheet.insert_image(row_num, data, {'image_data': imageData})
                y += 1
            else:
                for row_num, data in enumerate(titleList):
                    outSheet.write(row_num + 1, 0, data)
                for row_num, data in enumerate(priceList):
                    outSheet.write(row_num + 1, 1, data)
                for row_num, data in enumerate(descriptionList):
                    outSheet.write(row_num + 1, 2, data)
                for row_num, data in enumerate(linkArticleList):
                    outSheet.write_string(row_num + 1, 3, data)

                t += 1
            k += 1
        n += 1
        outWorkBook.close()


if __name__ == "__main__":
    parser()

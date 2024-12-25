import matplotlib.pyplot as plt
import db
import day

def chart_create():
    data = day.get_DayOfTheWeekId() - 1
    vals = [db.dish_coincidence(data, db.get_menu(data)[0].text), db.dish_coincidence(data, db.get_menu(data)[1].text), db.dish_coincidence(data, db.get_menu(data)[2].text), db.dish_coincidence(data, db.get_menu(data)[3].text)]
    labels = [db.get_menu(data)[0].text, db.get_menu(data)[1].text, db.get_menu(data)[2].text, db.get_menu(data)[3].text]
    color = ("#FA6F46", "#0BADA4", "#3B3A92", "#ACABAB")
    plt.pie(vals, labels=labels, colors=color, autopct='%1.1f%%')
    plt.savefig('my_plot.png')
    return sum(vals)

# chart_create()    
# plt.show()
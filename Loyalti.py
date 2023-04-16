def get_loyalty(loyaltyValue):
    match (loyaltyValue):
        case "0":
            return "Отсутствует"
        case "5":
            return "Бронзовая карта"
        case "10":
            return "Серебряная карта"
        case "20":
            return "Золотая карта"
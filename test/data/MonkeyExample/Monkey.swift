class Monkey {
    var consumedBananas = [Banana]()

    func eat(_ banana: Banana) {
        print("Eating the \(banana.color) banana")
        consumedBananas.append(banana)
    }

    func give(banana: Banana, toMonkey monkey: Monkey) {
        // ...
    }
}

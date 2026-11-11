import SwiftUI

/// «مصحف الشواهد» (مصحف ورش مع شواهد مورد الظمآن) as a native iPhone / iPad app.
/// The app shows the same web app that lives on GitHub Pages, so every update reaches it by itself.
/// After the first launch it opens without internet (the page and every opened book page are kept on the device).
@main
struct MawridApp: App {
    init() { RenewalReminder.schedule() }   // تذكير التجديد قبل انتهاء الأيام السبعة

    var body: some Scene {
        WindowGroup {
            WebContainer()
                .onOpenURL { MawridLink.receive($0) }   // بيت مطلوب من «خزانتي»
                .ignoresSafeArea()
                .overlay(RenewalIndicator(appName: "مصحف الشواهد", current: "shawahid"))   // زر «تطبيقاتي» العائم وعدّاد أيام التجديد
                .background(Color(red: 0.961, green: 0.969, blue: 0.980).ignoresSafeArea())
        }
    }
}

struct WebContainer: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> WebViewController { WebViewController() }
    func updateUIViewController(_ controller: WebViewController, context: Context) {}
}

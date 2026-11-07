import SwiftUI

/// «مورد الظمآن» as a native iPhone / iPad app.
/// The app shows the same web app that lives on GitHub Pages, so every update reaches it by itself.
/// After the first launch it opens without internet (the page and every opened book page are kept on the device).
@main
struct MawridApp: App {
    init() { RenewalReminder.schedule() }   // تذكير التجديد قبل انتهاء الأيام السبعة

    var body: some Scene {
        WindowGroup {
            WebContainer()
                .ignoresSafeArea()
                .overlay(RenewalIndicator(appName: "مورد الظمآن"))   // نقطة الأيام الباقية للتجديد
                .background(Color(red: 0.965, green: 0.945, blue: 0.906).ignoresSafeArea())
        }
    }
}

struct WebContainer: UIViewControllerRepresentable {
    func makeUIViewController(context: Context) -> WebViewController { WebViewController() }
    func updateUIViewController(_ controller: WebViewController, context: Context) {}
}

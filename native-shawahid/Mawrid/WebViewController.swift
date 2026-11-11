import UIKit
import WebKit

let appURL = URL(string: "https://khaledkadoum86-sudo.github.io/mawrid/mushaf/")!
let appHost = "khaledkadoum86-sudo.github.io"
private let pageBackground = UIColor(red: 0.961, green: 0.969, blue: 0.980, alpha: 1)   // #F5F7FA لون التطبيقات الموحّد

/// رابط بيت وصل من «خزانتي»: mawrid://verse?id=r:23 ← تفتح الصفحة البيت مباشرة.
enum MawridLink {
    static let arrived = Notification.Name("MawridVerseLink")
    static var pending: String?

    static func receive(_ url: URL) {
        guard url.host == "verse",
              let id = URLComponents(url: url, resolvingAgainstBaseURL: false)?.queryItems?.first(where: { $0.name == "id" })?.value,
              id.range(of: "^[a-z]:[0-9]{1,4}$", options: .regularExpression) != nil else { return }
        pending = id
        NotificationCenter.default.post(name: arrived, object: nil)
    }
}

final class WebViewController: UIViewController, WKNavigationDelegate, WKUIDelegate {
    private var webView: WKWebView!
    private var offlineView: UIView?

    override func loadView() {
        let config = WKWebViewConfiguration()
        // App-bound domains: lets the page keep itself on the device (service worker) so it opens offline.
        config.limitsNavigationsToAppBoundDomains = true
        config.websiteDataStore = .default()
        config.applicationNameForUserAgent = "Mobile/15E148 ShawahidApp"
        config.userContentController.addUserScript(WKUserScript(source: "window.MAWRID_NATIVE=true;", injectionTime: .atDocumentStart, forMainFrameOnly: true))

        webView = WKWebView(frame: .zero, configuration: config)
        webView.navigationDelegate = self
        webView.uiDelegate = self
        webView.allowsBackForwardNavigationGestures = false
        webView.allowsLinkPreview = false
        webView.scrollView.contentInsetAdjustmentBehavior = .never
        webView.isOpaque = false
        webView.backgroundColor = pageBackground
        webView.scrollView.backgroundColor = pageBackground
        view = webView
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        webView.load(URLRequest(url: appURL))
        NotificationCenter.default.addObserver(self, selector: #selector(openPendingVerse), name: MawridLink.arrived, object: nil)
    }

    /// يفتح البيت المطلوب من «خزانتي» (المعرّف مفحوص في MawridLink فلا يحمل غير حرف ورقم).
    @objc private func openPendingVerse() {
        guard let id = MawridLink.pending, !webView.isLoading else { return }
        MawridLink.pending = nil
        webView.evaluateJavaScript("window.mawridOpen && mawridOpen('\(id)')", completionHandler: nil)
    }

    // MARK: - Links: the app stays inside, other sites open outside

    func webView(_ webView: WKWebView, decidePolicyFor navigationAction: WKNavigationAction, decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        guard let url = navigationAction.request.url else { decisionHandler(.cancel); return }
        let scheme = (url.scheme ?? "").lowercased()
        if ["blob", "data", "about"].contains(scheme) { decisionHandler(.allow); return }
        if Siblings.handle(url) { decisionHandler(.cancel); return }   // halaqa:// khizana:// mawrid://
        if scheme == "https" && url.host == appHost { decisionHandler(.allow); return }
        if navigationAction.targetFrame?.isMainFrame ?? true {
            UIApplication.shared.open(url)
            decisionHandler(.cancel)
            return
        }
        decisionHandler(.allow)
    }

    func webView(_ webView: WKWebView, createWebViewWith configuration: WKWebViewConfiguration, for navigationAction: WKNavigationAction, windowFeatures: WKWindowFeatures) -> WKWebView? {
        if let url = navigationAction.request.url {
            if url.host == appHost { webView.load(navigationAction.request) } else { UIApplication.shared.open(url) }
        }
        return nil
    }

    // MARK: - alert / confirm / prompt from the page

    func webView(_ webView: WKWebView, runJavaScriptAlertPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping () -> Void) {
        let alert = UIAlertController(title: nil, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "حسنًا", style: .default) { _ in completionHandler() })
        top().present(alert, animated: true)
    }

    func webView(_ webView: WKWebView, runJavaScriptConfirmPanelWithMessage message: String, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping (Bool) -> Void) {
        let alert = UIAlertController(title: nil, message: message, preferredStyle: .alert)
        alert.addAction(UIAlertAction(title: "إلغاء", style: .cancel) { _ in completionHandler(false) })
        alert.addAction(UIAlertAction(title: "موافق", style: .default) { _ in completionHandler(true) })
        top().present(alert, animated: true)
    }

    func webView(_ webView: WKWebView, runJavaScriptTextInputPanelWithPrompt prompt: String, defaultText: String?, initiatedByFrame frame: WKFrameInfo, completionHandler: @escaping (String?) -> Void) {
        let alert = UIAlertController(title: nil, message: prompt, preferredStyle: .alert)
        alert.addTextField { $0.text = defaultText }
        alert.addAction(UIAlertAction(title: "إلغاء", style: .cancel) { _ in completionHandler(nil) })
        alert.addAction(UIAlertAction(title: "موافق", style: .default) { _ in completionHandler(alert.textFields?.first?.text) })
        top().present(alert, animated: true)
    }

    // MARK: - No internet on the very first launch

    func webView(_ webView: WKWebView, didFailProvisionalNavigation navigation: WKNavigation!, withError error: Error) {
        let code = (error as NSError).code
        if code == NSURLErrorCancelled || code == 102 { return }
        if webView.url == nil || webView.url?.host != appHost || !webView.canGoBack { showOffline() }
    }

    func webView(_ webView: WKWebView, didFinish navigation: WKNavigation!) {
        offlineView?.removeFromSuperview()
        offlineView = nil
        openPendingVerse()
    }

    func webViewWebContentProcessDidTerminate(_ webView: WKWebView) {
        webView.reload()
    }

    private func showOffline() {
        guard offlineView == nil else { return }
        let box = UIView(frame: view.bounds)
        box.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        box.backgroundColor = pageBackground

        let label = UILabel()
        label.text = "لا يوجد اتصال بالإنترنت.\nيحتاج التطبيق إلى الإنترنت عند أول تشغيل فقط، ثم يعمل دونه."
        label.numberOfLines = 0
        label.textAlignment = .center
        label.font = .systemFont(ofSize: 17, weight: .semibold)
        label.textColor = UIColor(red: 0.06, green: 0.12, blue: 0.2, alpha: 1)

        let button = UIButton(type: .system)
        button.setTitle("إعادة المحاولة", for: .normal)
        button.titleLabel?.font = .systemFont(ofSize: 18, weight: .bold)
        button.addTarget(self, action: #selector(retry), for: .touchUpInside)

        let stack = UIStackView(arrangedSubviews: [label, button])
        stack.axis = .vertical
        stack.spacing = 18
        stack.translatesAutoresizingMaskIntoConstraints = false
        box.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.centerYAnchor.constraint(equalTo: box.centerYAnchor),
            stack.leadingAnchor.constraint(equalTo: box.leadingAnchor, constant: 28),
            stack.trailingAnchor.constraint(equalTo: box.trailingAnchor, constant: -28),
        ])
        view.addSubview(box)
        offlineView = box
    }

    @objc private func retry() {
        offlineView?.removeFromSuperview()
        offlineView = nil
        webView.load(URLRequest(url: appURL))
    }

    private func top() -> UIViewController {
        var controller: UIViewController = self
        while let next = controller.presentedViewController { controller = next }
        return controller
    }
}

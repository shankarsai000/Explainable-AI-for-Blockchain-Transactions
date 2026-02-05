export default function Header() {
    return (
        <header className="glass border-b border-white/5 sticky top-0 z-50">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex items-center justify-between h-16">
                    {/* Logo */}
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary-500 to-accent-500 flex items-center justify-center">
                            <span className="text-xl">⛓️</span>
                        </div>
                        <div>
                            <h1 className="text-lg font-bold text-white">TxExplainer</h1>
                            <p className="text-xs text-gray-500">AI-Powered Analysis</p>
                        </div>
                    </div>

                    {/* Navigation */}
                    <nav className="hidden md:flex items-center gap-6">
                        <a href="#" className="text-gray-400 hover:text-white transition-colors text-sm">
                            Documentation
                        </a>
                        <a href="#" className="text-gray-400 hover:text-white transition-colors text-sm">
                            API
                        </a>
                        <a
                            href="https://github.com"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-gray-400 hover:text-white transition-colors text-sm"
                        >
                            GitHub
                        </a>
                    </nav>

                    {/* Status Indicator */}
                    <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse"></div>
                        <span className="text-xs text-gray-500 hidden sm:inline">Ethereum Mainnet</span>
                    </div>
                </div>
            </div>
        </header>
    )
}

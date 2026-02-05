export default function LoadingState() {
    return (
        <div className="space-y-6">
            {/* Main Panel Skeleton */}
            <div className="glass rounded-2xl overflow-hidden">
                <div className="bg-gradient-to-r from-primary-600/10 to-accent-600/10 px-6 py-4">
                    <div className="skeleton h-6 w-48 rounded mb-2" />
                    <div className="skeleton h-4 w-96 rounded" />
                </div>

                <div className="p-6">
                    <div className="grid grid-cols-4 gap-4 mb-6">
                        {[...Array(4)].map((_, i) => (
                            <div key={i} className="glass-light rounded-xl p-4">
                                <div className="skeleton h-3 w-16 rounded mb-2" />
                                <div className="skeleton h-8 w-24 rounded mb-1" />
                                <div className="skeleton h-3 w-12 rounded" />
                            </div>
                        ))}
                    </div>

                    <div className="skeleton h-24 rounded-xl" />
                </div>
            </div>

            {/* Charts Skeleton */}
            <div className="grid grid-cols-2 gap-6">
                {[...Array(2)].map((_, i) => (
                    <div key={i} className="glass rounded-2xl p-6">
                        <div className="skeleton h-5 w-40 rounded mb-4" />
                        <div className="skeleton h-48 rounded-xl" />
                    </div>
                ))}
            </div>

            {/* Loading Indicator */}
            <div className="flex items-center justify-center py-8">
                <div className="flex items-center gap-3 text-gray-400">
                    <div className="relative">
                        <div className="w-12 h-12 border-4 border-primary-500/20 rounded-full" />
                        <div className="absolute top-0 left-0 w-12 h-12 border-4 border-transparent border-t-primary-500 rounded-full animate-spin" />
                    </div>
                    <div>
                        <p className="font-medium text-white">Analyzing Transaction</p>
                        <p className="text-sm">Running ML models...</p>
                    </div>
                </div>
            </div>
        </div>
    )
}

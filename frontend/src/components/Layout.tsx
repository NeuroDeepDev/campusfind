import { Outlet, Link } from 'react-router-dom'
import { useAuthStore } from '@/stores/authStore'

export default function Layout() {
  const { user, logout } = useAuthStore()

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <Link to="/" className="text-2xl font-bold text-blue-600">
            CampusFind
          </Link>

          <div className="flex gap-4 items-center">
            <Link to="/dashboard" className="text-gray-600 hover:text-gray-800">
              Dashboard
            </Link>
            <Link to="/search" className="text-gray-600 hover:text-gray-800">
              Search
            </Link>
            {user?.email?.includes('admin') && (
              <Link to="/admin" className="text-gray-600 hover:text-gray-800">
                Admin
              </Link>
            )}
            <div className="flex items-center gap-2">
              <span className="text-sm text-gray-600">{user?.first_name}</span>
              <button
                onClick={() => {
                  logout()
                  window.location.href = '/login'
                }}
                className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      <main className="max-w-7xl mx-auto">
        <Outlet />
      </main>
    </div>
  )
}

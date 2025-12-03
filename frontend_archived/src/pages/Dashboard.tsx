import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { itemsApi } from '@/services/api'

export default function Dashboard() {
  const [foundItems, setFoundItems] = useState<any[]>([])
  const [lostItems, setLostItems] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('found')

  useEffect(() => {
    const fetchItems = async () => {
      try {
        const [foundRes, lostRes] = await Promise.all([
          itemsApi.foundItems(),
          itemsApi.lostItems(),
        ])
        setFoundItems(foundRes.data)
        setLostItems(lostRes.data)
      } catch (error) {
        console.error('Failed to fetch items')
      } finally {
        setLoading(false)
      }
    }

    fetchItems()
  }, [])

  const items = activeTab === 'found' ? foundItems : lostItems

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Dashboard</h1>

      <div className="mb-6 flex gap-4">
        <button
          onClick={() => setActiveTab('found')}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === 'found'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-800'
          }`}
        >
          Found Items
        </button>
        <button
          onClick={() => setActiveTab('lost')}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === 'lost'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-800'
          }`}
        >
          Lost Items
        </button>
        <Link to="/search" className="px-4 py-2 bg-green-600 text-white rounded font-semibold">
          Search
        </Link>
      </div>

      {loading ? (
        <div className="text-center">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {items.map((item) => (
            <Link
              key={item.id}
              to={`/items/${item.id}`}
              className="bg-white rounded-lg shadow-md p-4 hover:shadow-lg transition"
            >
              <h3 className="font-bold text-lg mb-2">{item.name}</h3>
              <p className="text-gray-600 text-sm mb-2">{item.description}</p>
              <div className="flex justify-between text-xs text-gray-500">
                <span>{item.category_name}</span>
                <span>{item.location_name}</span>
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}

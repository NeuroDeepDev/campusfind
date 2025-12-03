import { useState, useEffect } from 'react'
import { itemsApi } from '@/services/api'

export default function SearchItems() {
  const [items, setItems] = useState<any[]>([])
  const [searchQuery, setSearchQuery] = useState('')
  const [filter, setFilter] = useState('all')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    const searchItems = async () => {
      if (searchQuery.length < 2 && filter === 'all') return

      setLoading(true)
      try {
        const response = await itemsApi.list({
          search: searchQuery,
          item_type: filter === 'all' ? '' : filter,
        })
        setItems(response.data.results || response.data)
      } catch (error) {
        console.error('Search failed')
      } finally {
        setLoading(false)
      }
    }

    const timer = setTimeout(searchItems, 500)
    return () => clearTimeout(timer)
  }, [searchQuery, filter])

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Search Items</h1>

      <div className="mb-6 space-y-4">
        <input
          type="text"
          placeholder="Search items by name or description..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
        />

        <div className="flex gap-2">
          {['all', 'Found', 'Lost'].map((type) => (
            <button
              key={type}
              onClick={() => setFilter(type)}
              className={`px-4 py-2 rounded font-semibold ${
                filter === type
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {type === 'all' ? 'All' : type}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="text-center">Searching...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {items.map((item) => (
            <div
              key={item.id}
              className="bg-white rounded-lg shadow-md p-4 cursor-pointer hover:shadow-lg"
              onClick={() => (window.location.href = `/items/${item.id}`)}
            >
              <h3 className="font-bold text-lg mb-2">{item.name}</h3>
              <p className="text-gray-600 text-sm mb-3">{item.description}</p>
              <div className="flex justify-between text-xs text-gray-500">
                <span className="bg-gray-100 px-2 py-1 rounded">{item.status}</span>
                <span>{item.category_name}</span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

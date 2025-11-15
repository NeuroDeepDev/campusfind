import { useState, useEffect } from 'react'
import { useParams } from 'react-router-dom'
import { itemsApi, claimsApi } from '@/services/api'
import { useAuthStore } from '@/stores/authStore'

export default function ItemDetail() {
  const { id } = useParams()
  const [item, setItem] = useState<any>(null)
  const [loading, setLoading] = useState(true)
  const [claimDescription, setClaimDescription] = useState('')
  const [showClaimForm, setShowClaimForm] = useState(false)
  const user = useAuthStore((state) => state.user)

  useEffect(() => {
    const fetchItem = async () => {
      try {
        const response = await itemsApi.get(Number(id))
        setItem(response.data)
      } catch (error) {
        console.error('Failed to fetch item')
      } finally {
        setLoading(false)
      }
    }

    fetchItem()
  }, [id])

  const handleClaim = async (e: React.FormEvent) => {
    e.preventDefault()

    try {
      const formData = new FormData()
      formData.append('item', String(item.id))
      formData.append('claim_description', claimDescription)

      await claimsApi.create(formData)
      setShowClaimForm(false)
      setClaimDescription('')
      alert('Claim created successfully!')
    } catch (error) {
      console.error('Failed to create claim')
      alert('Failed to create claim')
    }
  }

  if (loading) return <div className="p-4 text-center">Loading...</div>
  if (!item) return <div className="p-4 text-center">Item not found</div>

  const canClaim = item.status === 'Found' && item.item_type === 'Found'

  return (
    <div className="max-w-2xl mx-auto p-4">
      <div className="bg-white rounded-lg shadow-lg p-6">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">{item.name}</h1>

        <div className="grid grid-cols-2 gap-4 mb-6 text-sm">
          <div>
            <p className="text-gray-600">Type</p>
            <p className="font-semibold text-lg">{item.item_type}</p>
          </div>
          <div>
            <p className="text-gray-600">Status</p>
            <p className="font-semibold text-lg">{item.status}</p>
          </div>
          <div>
            <p className="text-gray-600">Category</p>
            <p className="font-semibold">{item.category_name}</p>
          </div>
          <div>
            <p className="text-gray-600">Location</p>
            <p className="font-semibold">{item.location_name}</p>
          </div>
        </div>

        <div className="mb-6">
          <p className="text-gray-600 mb-2">Description</p>
          <p className="text-gray-800">{item.description}</p>
        </div>

        {item.evidence_file && (
          <div className="mb-6">
            <p className="text-gray-600 mb-2">Evidence</p>
            <a
              href={item.evidence_file}
              target="_blank"
              rel="noreferrer"
              className="text-blue-600 hover:underline"
            >
              View File
            </a>
          </div>
        )}

        {canClaim && (
          <div>
            <button
              onClick={() => setShowClaimForm(!showClaimForm)}
              className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            >
              {showClaimForm ? 'Cancel' : 'Claim This Item'}
            </button>

            {showClaimForm && (
              <form onSubmit={handleClaim} className="mt-4 p-4 bg-gray-50 rounded">
                <textarea
                  value={claimDescription}
                  onChange={(e) => setClaimDescription(e.target.value)}
                  placeholder="Describe why this is your item..."
                  required
                  className="w-full px-4 py-2 border border-gray-300 rounded mb-4 focus:outline-none focus:ring-2 focus:ring-green-500"
                  rows={4}
                />
                <button
                  type="submit"
                  className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
                >
                  Submit Claim
                </button>
              </form>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

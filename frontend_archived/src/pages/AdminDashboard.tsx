import { useState, useEffect } from 'react'
import { claimsApi, auditApi } from '@/services/api'

export default function AdminDashboard() {
  const [claims, setClaims] = useState<any[]>([])
  const [audits, setAudits] = useState<any[]>([])
  const [activeTab, setActiveTab] = useState('claims')
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true)
      try {
        const [claimsRes, auditsRes] = await Promise.all([
          claimsApi.pending(),
          auditApi.list(),
        ])
        setClaims(claimsRes.data)
        setAudits(auditsRes.data.results || auditsRes.data)
      } catch (error) {
        console.error('Failed to fetch admin data')
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const handleApproveClaim = async (claimId: number) => {
    try {
      await claimsApi.approve(claimId)
      setClaims(claims.filter((c) => c.id !== claimId))
      alert('Claim approved!')
    } catch (error) {
      alert('Failed to approve claim')
    }
  }

  const handleRejectClaim = async (claimId: number) => {
    try {
      await claimsApi.reject(claimId)
      setClaims(claims.filter((c) => c.id !== claimId))
      alert('Claim rejected!')
    } catch (error) {
      alert('Failed to reject claim')
    }
  }

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-6">Admin Dashboard</h1>

      <div className="mb-6 flex gap-4">
        <button
          onClick={() => setActiveTab('claims')}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === 'claims'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-800'
          }`}
        >
          Pending Claims
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`px-4 py-2 rounded font-semibold ${
            activeTab === 'audit'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-200 text-gray-800'
          }`}
        >
          Audit Log
        </button>
      </div>

      {loading ? (
        <div className="text-center">Loading...</div>
      ) : activeTab === 'claims' ? (
        <div className="space-y-4">
          {claims.length === 0 ? (
            <p className="text-gray-600">No pending claims</p>
          ) : (
            claims.map((claim) => (
              <div key={claim.id} className="bg-white rounded-lg shadow-md p-4">
                <h3 className="font-bold text-lg mb-2">{claim.item_name}</h3>
                <p className="text-gray-600 mb-2">{claim.claim_description}</p>
                <p className="text-sm text-gray-500 mb-4">Claimed by: {claim.claimed_by_name}</p>
                <div className="flex gap-2">
                  <button
                    onClick={() => handleApproveClaim(claim.id)}
                    className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700"
                  >
                    Approve
                  </button>
                  <button
                    onClick={() => handleRejectClaim(claim.id)}
                    className="px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700"
                  >
                    Reject
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      ) : (
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-gray-200">
              <tr>
                <th className="px-4 py-2 text-left">Action</th>
                <th className="px-4 py-2 text-left">Table</th>
                <th className="px-4 py-2 text-left">ID</th>
                <th className="px-4 py-2 text-left">Changed By</th>
                <th className="px-4 py-2 text-left">Created At</th>
              </tr>
            </thead>
            <tbody>
              {audits.map((audit) => (
                <tr key={audit.id} className="border-b">
                  <td className="px-4 py-2">{audit.action}</td>
                  <td className="px-4 py-2">{audit.affected_table}</td>
                  <td className="px-4 py-2">{audit.affected_id}</td>
                  <td className="px-4 py-2">{audit.changed_by_name || 'System'}</td>
                  <td className="px-4 py-2">{new Date(audit.created_at).toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}

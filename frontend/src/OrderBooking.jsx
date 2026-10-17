
import { useEffect, useState } from 'react'

function OrderBooking() {
  const [services, setServices] = useState([])
  const [addresses, setAddresses] = useState([])
  const [addressLoading, setAddressLoading] = useState(true)
  const [serviceId, setServiceId] = useState('')
  const [addressId, setAddressId] = useState('')
  const [quantity, setQuantity] = useState('1')
  const [garmentType, setGarmentType] = useState('')
  const [expectedDate, setExpectedDate] = useState('')
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/services/', {
      credentials: 'include',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Could not load services')
        }
        return response.json()
      })
      .then((data) => {
        setServices(data)

        if (data.length > 0) {
          setServiceId(String(data[0].id))
        }
      })
      .catch(() => {
        setError('Services could not be loaded. Please try again.')
      })
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    fetch('/api/addresses/', {
      credentials: 'include',
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error('Could not load addresses')
        }
        return response.json()
      })
      .then((data) => {
        setAddresses(data)

        if (data.length > 0) {
          setAddressId(String(data[0].id))
        }
      })
      .catch(() => {
        setError(
          'Addresses could not be loaded. Please check your login.'
        )
      })
      .finally(() => setAddressLoading(false))
  }, [])

  const selectedService = services.find(
    (service) => String(service.id) === serviceId
  )

  const total =
    selectedService && quantity !== ''
      ? Number(selectedService.price) * Number(quantity)
      : 0

  const today = new Date().toLocaleDateString('en-CA')

  return (
    <main className="min-h-screen bg-slate-50 px-4 py-12 text-slate-800">
      <div className="mx-auto max-w-2xl">
        <a
          href="/"
          className="font-semibold text-purple-700 hover:underline"
        >
          ← Back to Home
        </a>

        <section className="mt-6 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm sm:p-8">
          <p className="text-sm font-bold uppercase tracking-widest text-purple-700">
            LaundryCare
          </p>

          <h1 className="mt-2 text-3xl font-extrabold">
            Book a Laundry Service
          </h1>

          <p className="mt-3 text-slate-600">
            Select a service, address, garment type and quantity to
            calculate your estimated bill.
          </p>

          {loading && (
            <p className="mt-6" role="status">
              Loading services...
            </p>
          )}

          {error && (
            <p className="mt-6 text-red-600" role="alert">
              {error}
            </p>
          )}

          {!loading && !error && services.length === 0 && (
            <p className="mt-6 text-amber-700">
              No services are currently available.
            </p>
          )}

          {!loading && !error && services.length > 0 && (
            <form
              className="mt-8 space-y-6"
              onSubmit={async (event) => {
                event.preventDefault()
                setError('')

                try {
                  const csrfResponse = await fetch('/api/csrf/', {
                    credentials: 'include',
                  })

                  if (!csrfResponse.ok) {
                    throw new Error(
                      'Could not prepare secure booking request.'
                    )
                  }

                  const csrfToken = document.cookie
                    .split('; ')
                    .find((cookie) =>
                      cookie.startsWith('csrftoken=')
                    )
                    ?.split('=')[1]

                  if (!csrfToken) {
                    throw new Error(
                      'Security token not found. Please refresh and try again.'
                    )
                  }

                  const formData = new URLSearchParams()

                  formData.append('service', serviceId)
                  formData.append('address', addressId)
                  formData.append(
                    'garment_type',
                    garmentType.trim()
                  )
                  formData.append('quantity', quantity)
                  formData.append('expected_date', expectedDate)

                  const response = await fetch('/api/orders/', {
                    method: 'POST',
                    credentials: 'include',
                    headers: {
                      'Content-Type':
                        'application/x-www-form-urlencoded;charset=UTF-8',
                      'X-CSRFToken': decodeURIComponent(csrfToken),
                    },
                    body: formData.toString(),
                  })

                  const data = await response.json()

                  if (!response.ok) {
                    throw new Error(
                      data.error || 'Unable to place the order.'
                    )
                  }

                  window.location.href = '/dashboard/'
                } catch (err) {
                  setError(
                    err.message ||
                      'Something went wrong. Please try again.'
                  )
                }
              }}
            >
              <div>
                <label
                  htmlFor="address"
                  className="mb-2 block font-semibold"
                >
                  Select Address
                </label>

                {addressLoading ? (
                  <p>Loading addresses...</p>
                ) : addresses.length === 0 ? (
                  <p className="text-amber-700">
                    No saved addresses found. Please log in and add
                    an address to your profile.
                  </p>
                ) : (
                  <select
                    id="address"
                    value={addressId}
                    onChange={(event) => {
                      setAddressId(event.target.value)
                      setError('')
                    }}
                    required
                    className="w-full rounded-lg border border-slate-300 px-4 py-3"
                  >
                    {addresses.map((address) => (
                      <option
                        key={address.id}
                        value={address.id}
                      >
                        {address.address_line}, {address.city} -{' '}
                        {address.pincode}
                      </option>
                    ))}
                  </select>
                )}
              </div>

              <div>
                <label
                  htmlFor="service"
                  className="mb-2 block font-semibold"
                >
                  Select Service
                </label>

                <select
                  id="service"
                  value={serviceId}
                  onChange={(event) => {
                    setServiceId(event.target.value)
                    setError('')
                  }}
                  required
                  className="w-full rounded-lg border border-slate-300 px-4 py-3"
                >
                  {services.map((service) => (
                    <option
                      key={service.id}
                      value={service.id}
                    >
                      {service.name} — ₹{service.price} per item
                    </option>
                  ))}
                </select>
              </div>

              <div>
                <label
                  htmlFor="garment"
                  className="mb-2 block font-semibold"
                >
                  Garment Type
                </label>

                <input
                  id="garment"
                  type="text"
                  value={garmentType}
                  onChange={(event) => {
                    setGarmentType(event.target.value)
                    setError('')
                  }}
                  placeholder="e.g. Shirt, Trousers, Saree"
                  required
                  maxLength={100}
                  className="w-full rounded-lg border border-slate-300 px-4 py-3"
                />
              </div>

              <div>
                <label
                  htmlFor="quantity"
                  className="mb-2 block font-semibold"
                >
                  Quantity
                </label>

                <input
                  id="quantity"
                  type="number"
                  min="1"
                  max="100"
                  step="1"
                  value={quantity}
                  onChange={(event) => {
                    setQuantity(event.target.value)
                    setError('')
                  }}
                  required
                  className="w-full rounded-lg border border-slate-300 px-4 py-3"
                />

                <p className="mt-1 text-sm text-slate-500">
                  Enter a quantity between 1 and 100.
                </p>
              </div>

              <div>
                <label
                  htmlFor="expectedDate"
                  className="mb-2 block font-semibold"
                >
                  Expected Date
                </label>

                <input
                  id="expectedDate"
                  type="date"
                  min={today}
                  value={expectedDate}
                  onChange={(event) => {
                    setExpectedDate(event.target.value)
                    setError('')
                  }}
                  required
                  className="w-full rounded-lg border border-slate-300 px-4 py-3"
                />
              </div>

              <div className="rounded-xl bg-purple-50 p-5">
                <p className="text-sm font-medium text-slate-600">
                  Estimated Total
                </p>

                <p className="mt-1 text-3xl font-extrabold text-purple-800">
                  ₹{total.toFixed(2)}
                </p>

                <p className="mt-2 text-sm text-slate-600">
                  {selectedService?.name || 'Select a service'} ×{' '}
                  {quantity || 0} item(s)
                </p>
              </div>

              {error && (
                <p
                  role="alert"
                  className="text-sm text-amber-700"
                >
                  {error}
                </p>
              )}

              <button
                type="submit"
                disabled={
                  !selectedService ||
                  !addressId ||
                  addresses.length === 0 ||
                  !Number.isInteger(Number(quantity)) ||
                  Number(quantity) < 1 ||
                  Number(quantity) > 100 ||
                  !garmentType.trim() ||
                  !expectedDate
                }
                className="w-full rounded-lg bg-purple-700 px-5 py-3 font-bold text-white hover:bg-purple-800 disabled:cursor-not-allowed disabled:opacity-50"
              >
                Place Order
              </button>
            </form>
          )}
        </section>
      </div>
    </main>
  )
}

export default OrderBooking


import { useEffect, useState } from 'react'
import OrderBooking from './OrderBooking.jsx'

function App() {
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [showBooking, setShowBooking] = useState(false)

  useEffect(() => {
    fetch('/api/services/')
      .then((response) => {
        if (!response.ok) throw new Error('Unable to load services')
        return response.json()
      })
      .then((data) => setServices(data))
      .catch(() => setError('Services could not be loaded. Please try again.'))
      .finally(() => setLoading(false))
  }, [])

  if (showBooking) return <OrderBooking />

  return (
    <div className="min-h-screen bg-[#F3F9F4] text-slate-800">
      {/* Navigation */}
      <header className="sticky top-0 z-20 border-b border-emerald-100 bg-white/95 shadow-sm backdrop-blur">
        <nav className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3 md:px-8">
          <a href="/" className="flex items-center gap-2 text-xl font-extrabold text-emerald-900 sm:text-2xl">
            <span className="flex h-10 w-10 items-center justify-center rounded-xl bg-emerald-100 text-2xl">🧺</span>
            LaundryCare
          </a>

          <div className="flex items-center gap-2 sm:gap-4">
            <a href="#services" className="hidden rounded-full bg-emerald-50 px-4 py-2 text-sm font-bold text-emerald-800 hover:bg-emerald-100 sm:block">
              Services
            </a>
            <a href="http://127.0.0.1:8000/" className="hidden rounded-full bg-emerald-50 px-4 py-2 text-sm font-bold text-emerald-800 hover:bg-emerald-100 sm:block">
              About Us
            </a>
            <a href="http://127.0.0.1:8000/login/" className="rounded-xl bg-emerald-700 px-4 py-2.5 text-sm font-bold text-white shadow-md transition hover:bg-emerald-800">
              Login
            </a>
            <a href="http://127.0.0.1:8000/register/" className="rounded-xl bg-emerald-900 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-emerald-950">
              Register
            </a>
          </div>
        </nav>
      </header>

      <main>
        {/* Photo background hero */}
        <section className="relative isolate overflow-hidden">
          <div
            className="absolute inset-0 -z-20 bg-cover bg-center"
            style={{
          
                backgroundImage: "url('/laundry-background.png')",
            }}
          />
          <div className="absolute inset-0 -z-10 bg-gradient-to-r from-[#E8F7EC]/65 via-[#E8F7EC]/40 to-[#E8F7EC]/15" />
          <div className="absolute inset-0 -z-10 bg-white/10" />

          {/* Single-column hero: no white journey card */}
          <div className="relative mx-auto flex min-h-[390px] max-w-7xl items-center px-5 py-12 md:min-h-[440px] md:px-8 md:py-16">
            <div className="max-w-2xl">
              <span className="inline-flex items-center gap-2 rounded-full border border-emerald-200 bg-white/85 px-4 py-2 text-xs font-extrabold uppercase tracking-widest text-emerald-900 shadow-sm">
                <span className="h-2 w-2 rounded-full bg-emerald-500" />
                Fresh clothes, less stress
              </span>

              <h1 className="mt-5 text-4xl font-black leading-tight tracking-tight text-emerald-950 sm:text-5xl md:text-6xl">
                Clean Clothes,
                <span className="mt-1 block text-emerald-700">Happier Days.</span>
              </h1>

              <p className="mt-5 max-w-xl text-base leading-7 text-slate-700 sm:text-lg">
                Professional laundry and dry-cleaning services that make
                everyday life easier. Enjoy fresh clothes, less effort and
                more time for what matters.
              </p>

              <div className="mt-7 flex flex-wrap gap-3">
                <button
                  type="button"
                  onClick={() => setShowBooking(true)}
                  className="rounded-xl bg-emerald-800 px-6 py-3.5 font-bold text-white shadow-lg shadow-emerald-900/20 transition hover:-translate-y-0.5 hover:bg-emerald-950"
                >
                  Book Your Service →
                </button>
                <a
                  href="#services"
                  className="rounded-xl border border-emerald-300 bg-white/90 px-6 py-3.5 font-bold text-emerald-900 shadow-sm transition hover:bg-emerald-50"
                >
                  Explore Services
                </a>
              </div>

              <div className="mt-6 flex flex-wrap gap-x-5 gap-y-2 text-sm font-semibold text-emerald-950">
                <span>✓ Quality Care</span>
                <span>✓ Easy Ordering</span>
                <span>✓ Order Tracking</span>
              </div>
            </div>
          </div>
        </section>

        {/* Services */}
        <section id="services" className="mx-auto max-w-7xl px-5 py-12 md:px-8 md:py-16">
          <div className="mx-auto max-w-2xl text-center">
            <span className="text-xs font-extrabold uppercase tracking-[0.2em] text-emerald-700">
              What we offer
            </span>
            <h2 className="mt-3 text-3xl font-extrabold tracking-tight text-emerald-950 md:text-4xl">
              Our Laundry Services
            </h2>
            <p className="mt-4 leading-7 text-slate-600">
              Thoughtful care for every garment, from everyday washing to special cleaning.
            </p>
          </div>

          {loading && (
            <p className="mt-10 text-center text-slate-500">Loading services...</p>
          )}

          {error && (
            <p role="alert" className="mt-10 text-center text-red-600">{error}</p>
          )}

          {!loading && !error && services.length === 0 && (
            <p className="mt-10 text-center text-slate-500">
              No services are available right now.
            </p>
          )}

          {!loading && !error && services.length > 0 && (
            <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
              {services.map((service, index) => (
                <article
                  key={service.id}
                  className="group rounded-3xl border border-emerald-100 bg-white p-6 shadow-sm transition duration-300 hover:-translate-y-1 hover:border-emerald-300 hover:shadow-xl hover:shadow-emerald-900/10 sm:p-7"
                >
                  <div className={`flex h-16 w-16 items-center justify-center rounded-2xl text-3xl ${
                    index % 3 === 0
                      ? 'bg-emerald-100'
                      : index % 3 === 1
                        ? 'bg-sky-100'
                        : 'bg-lime-100'
                  }`}>
                    {service.name.toLowerCase() === 'washing'
                      ? '🧺'
                      : service.name.toLowerCase() === 'drycleaning'
                        ? '👔'
                        : service.name.toLowerCase() === 'ironing'
                          ? '👕'
                          : '🫧'}
                  </div>

                  <h3 className="mt-5 text-xl font-extrabold text-emerald-950">
                    {service.name}
                  </h3>
                  <p className="mt-3 min-h-12 leading-7 text-slate-600">
                    {service.description || 'Professional care for your clothes.'}
                  </p>

                  <div className="mt-5 flex items-end justify-between gap-3 border-t border-emerald-50 pt-5">
                    <p className="text-xl font-extrabold text-emerald-700">
                      ₹{service.price}
                      <span className="mt-1 block text-xs font-medium text-slate-500">
                        per item
                      </span>
                    </p>
                    <button
                      type="button"
                      onClick={() => setShowBooking(true)}
                      className="rounded-xl bg-emerald-700 px-4 py-2.5 text-sm font-bold text-white shadow-sm transition hover:bg-emerald-800 sm:px-5"
                    >
                      Book Now →
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>

        {/* Booking call to action */}
        <section className="px-5 pb-12 md:px-8 md:pb-16">
          <div className="mx-auto flex max-w-7xl flex-col items-center justify-between gap-6 rounded-3xl bg-gradient-to-r from-emerald-900 via-emerald-800 to-teal-700 px-6 py-10 text-center text-white shadow-xl md:flex-row md:px-12 md:text-left">
            <div>
              <span className="text-xs font-bold uppercase tracking-[0.2em] text-emerald-100">
                A little more convenience
              </span>
              <h2 className="mt-3 text-2xl font-extrabold md:text-3xl">
                Ready to make laundry easier?
              </h2>
              <p className="mt-3 text-emerald-50">
                Give your clothes the care they deserve.
              </p>
            </div>
            <button
              type="button"
              onClick={() => setShowBooking(true)}
              className="shrink-0 rounded-xl bg-white px-6 py-3.5 font-extrabold text-emerald-900 shadow transition hover:bg-emerald-50"
            >
              Book Your Service →
            </button>
          </div>
        </section>
      </main>

      {/* Footer */}
      <footer className="border-t border-emerald-100 bg-white px-5 py-7 text-center">
        <a href="/" className="text-xl font-extrabold text-emerald-900">
          🧺 LaundryCare
        </a>
        <p className="mt-2 text-sm text-slate-500">
          Clean clothes. More time for what matters.
        </p>
        <div className="mt-4 flex flex-wrap justify-center gap-5 text-sm font-semibold text-slate-600">
          <a href="#services" className="hover:text-emerald-700">Services</a>
          <a href="http://127.0.0.1:8000/" className="hover:text-emerald-700">About Us</a>
          <a href="http://127.0.0.1:8000/login/" className="hover:text-emerald-700">Login</a>
          <a href="http://127.0.0.1:8000/register/" className="hover:text-emerald-700">Register</a>
        </div>
        <p className="mt-5 text-xs text-slate-400">
          © {new Date().getFullYear()} LaundryCare. All rights reserved.
        </p>
      </footer>
    </div>
  )
}

export default App

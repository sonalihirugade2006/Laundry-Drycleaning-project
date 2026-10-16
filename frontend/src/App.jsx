
import { useEffect, useState } from 'react'

function App() {
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/services/')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Unable to load services')
        }
        return response.json()
      })
      .then((data) => setServices(data))
      .catch(() => {
        setError('Services could not be loaded. Please try again.')
      })
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-slate-50 text-slate-800">
      <header className="bg-white shadow-sm">
        <nav className="mx-auto flex max-w-6xl items-center justify-between px-6 py-5">
          <a href="/" className="text-2xl font-extrabold text-purple-700">
            LaundryCare
          </a>

          <div className="flex items-center gap-5">
            <a href="#services" className="hidden text-sm font-medium hover:text-purple-700 sm:block">
              Services
            </a>
            <a
              href="http://127.0.0.1:8000/login/"
              className="rounded-lg bg-purple-700 px-5 py-2.5 text-sm font-semibold text-white hover:bg-purple-800"
            >
              Login
            </a>
          </div>
        </nav>
      </header>

      <main>
        <section className="bg-gradient-to-br from-purple-800 to-indigo-700 text-white">
          <div className="mx-auto grid max-w-6xl items-center gap-10 px-6 py-20 md:grid-cols-2 md:py-28">
            <div>
              <p className="mb-4 font-semibold uppercase tracking-widest text-purple-200">
                Fresh clothes, less stress
              </p>

              <h1 className="text-4xl font-extrabold leading-tight md:text-6xl">
                Clean Clothes,
                <span className="block text-purple-200">Happy You!</span>
              </h1>

              <p className="mt-6 max-w-lg text-lg leading-8 text-purple-100">
                Convenient laundry and dry-cleaning services to help you
                spend less time on chores and more time on what matters.
              </p>

              <a
                href="#services"
                className="mt-8 inline-block rounded-xl bg-white px-7 py-3.5 font-bold text-purple-800 shadow hover:bg-purple-50"
              >
                Explore Services
              </a>
            </div>

            <div className="rounded-3xl border border-white/20 bg-white/10 p-8 shadow-xl backdrop-blur-sm">
              <div className="text-7xl" aria-hidden="true">🧺</div>
              <h2 className="mt-6 text-2xl font-bold">
                Your laundry, simplified
              </h2>
              <p className="mt-3 leading-7 text-purple-100">
                Washing, dry cleaning and ironing—all in one convenient place.
              </p>
              <div className="mt-6 flex flex-wrap gap-3 text-sm">
                <span className="rounded-full bg-white/15 px-4 py-2">Quality Care</span>
                <span className="rounded-full bg-white/15 px-4 py-2">Easy Tracking</span>
                <span className="rounded-full bg-white/15 px-4 py-2">Simple Billing</span>
              </div>
            </div>
          </div>
        </section>

        <section id="services" className="mx-auto max-w-6xl px-6 py-16 md:py-20">
          <div className="text-center">
            <p className="font-semibold uppercase tracking-widest text-purple-700">
              What we offer
            </p>
            <h2 className="mt-3 text-3xl font-extrabold md:text-4xl">
              Our Services
            </h2>
            <p className="mx-auto mt-4 max-w-2xl leading-7 text-slate-600">
              Choose the care your clothes need. Our services are loaded
              directly from the LaundryCare database.
            </p>
          </div>

          {loading && (
            <p className="mt-10 text-center text-slate-600">
              Loading services...
            </p>
          )}

          {error && (
            <p role="alert" className="mt-10 text-center text-red-600">
              {error}
            </p>
          )}

          {!loading && !error && services.length === 0 && (
            <p className="mt-10 text-center text-slate-600">
              No services are available right now.
            </p>
          )}

          {!loading && !error && services.length > 0 && (
            <div className="mt-10 grid gap-6 sm:grid-cols-2 md:grid-cols-3">
              {services.map((service) => (
                <article
                  key={service.id}
                  className="rounded-2xl border border-slate-200 bg-white p-7 shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                >
                  <div className="flex h-14 w-14 items-center justify-center rounded-xl bg-purple-100 text-3xl">
                    {service.name.toLowerCase() === 'washing'
                      ? '🧺'
                      : service.name.toLowerCase() === 'drycleaning'
                        ? '👔'
                        : service.name.toLowerCase() === 'ironing'
                          ? '👕'
                          : '🧺'}
                  </div>
                  <h3 className="mt-5 text-xl font-bold text-slate-800">
                    {service.name}
                  </h3>
                  
                  <p className="mt-3 leading-6 text-slate-600">
                    {service.description || 'Professional care for your clothes.'}
                  </p>

                  <p className="mt-5 border-t border-slate-100 pt-4 text-lg font-bold text-purple-700">
                    ₹{service.price} <span className="text-sm font-medium text-slate-500">per item</span>
                  </p>

                </article>
              ))}
            </div>
          )}
        </section>

        <section className="bg-purple-50 px-6 py-14 text-center">
          <h2 className="text-2xl font-extrabold md:text-3xl">
            Ready to make laundry easier?
          </h2>
          <p className="mt-3 text-slate-600">
            Log in to access your LaundryCare account.
          </p>
          <a
            href="http://127.0.0.1:8000/login/"
            className="mt-6 inline-block rounded-lg bg-purple-700 px-7 py-3 font-semibold text-white hover:bg-purple-800"
          >
            Get Started
          </a>
        </section>
      </main>

      <footer className="bg-slate-900 px-6 py-6 text-center text-sm text-slate-300">
        © {new Date().getFullYear()} LaundryCare. All rights reserved.
      </footer>
    </div>
  )
}

export default App

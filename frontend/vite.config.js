
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/static/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/place-order/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/dashboard/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/my-orders/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/services/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/profile/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/logout/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/login/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/register/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/my-notifications/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/my-payments/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/my-deliveries/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/daily-orders-report/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/revenue-report/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
      '/order-tracking/': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})

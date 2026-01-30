import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: '野码AI - Agent性能基准测试平台',
  description: '统一的多AI Agent协作平台 + Agent性能基准测试',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-CN">
      <body>{children}</body>
    </html>
  )
}

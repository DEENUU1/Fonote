import Navbar from "@/components/Navbar";


// @ts-ignore
export default function Layout({ children }) {
  return (
    <>
      <section className="text-gray-700 h-screen body-font overflow-hidden border-t">
              <Navbar/>
        <main>{children}</main>
      </section>
    </>
  )
}
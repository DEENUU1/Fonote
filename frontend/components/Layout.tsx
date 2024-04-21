import Navbar from "@/components/Navbar";


// @ts-ignore
export default function Layout({ children }) {
  return (
    <>
    <Navbar/>
    <section className="text-gray-700 body-font overflow-hidden border-t border-gray-200">
      <main>{children}</main>
    </section>
</>

  )
}
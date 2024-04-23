import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar from "@/components/NavigationBar";
import Footer from "@/components/Footer";


// @ts-ignore
export default function Layout({ children }) {
  return (
    <>
      <Navbar/>
      <section className="text-gray-700 h-screen body-font overflow-hidden border-t">
          <ToastContainer/>
          <main>{children}</main>
      </section>
      <Footer/>
    </>
  )
}
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import Navbar from "@/components/NavigationBar";
import Footer from "@/components/Footer";


// @ts-ignore
export default function Layout({ children }) {
  return (
    <>
      <section className="text-gray-700 body-font overflow-hidden border-t">
      <Navbar/>

          <ToastContainer/>
          <main>{children}</main>
      </section>
      <Footer/>
    </>
  )
}
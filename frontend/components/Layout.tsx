import Navbar from "@/components/Navbar";
import {ToastContainer} from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


// @ts-ignore
export default function Layout({ children }) {
  return (
    <>
      <section className="text-gray-700 h-screen body-font overflow-hidden border-t">
          <ToastContainer/>
          <Navbar/>
        <main>{children}</main>
      </section>
    </>
  )
}
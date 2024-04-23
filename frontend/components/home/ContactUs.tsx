import Link from "next/link";

export const ContactUs = () => {
  return (
    <section className="py-10 bg-gray-100 sm:py-16 lg:py-20">
      <div className="px-4 mx-auto sm:px-6 lg:px-8 max-w-7xl">
        <div className="max-w-2xl mx-auto text-center">
          <h2 className="font-poppins text-3xl font-bold leading-tight text-gray-900 sm:text-4xl lg:text-5xl">
            Contact us
          </h2>
          <p className="max-w-xl mx-auto mt-4 text-base leading-relaxed text-gray-500">
            Get in Touch with Us Today to Elevate Your Recruitment Strategy
          </p>
        </div>

        <div className={""}>
          <Link href={"/contact"} className="inline-flex items-center justify-center w-full px-8 py-4 mt-10 font-semibold text-black bg-blue-500 hover:bg-blue-400 rounded-md">
            Contact us
          </Link>
        </div>

      </div>
    </section>
  );
};
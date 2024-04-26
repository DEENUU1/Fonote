import Layout from "@/components/Layout";
import {ContactForm} from "@/components/contact/ContactForm";
import React from "react";


export default function Contact() {

	return (
		<>
			<Layout>
				<main className={"h-screen"}>
					{
						<>
						<div className="my-6 mx-auto max-w-xl">
							<h1 className="text-3xl font-extrabold text-center">Contact</h1>
						</div>
						<ContactForm/>
						</>
					}
				</main>
			</Layout>
		</>
	);
}
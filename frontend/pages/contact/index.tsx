import Layout from "@/components/Layout";
import {ContactForm} from "@/components/contact/ContactForm";
import React from "react";
import HeaderText from "@/components/HeaderText";


export default function Contact() {

	return (
		<>
			<Layout>
				<main className={"h-screen"}>
					{
						<>
						<HeaderText text={"Contact"}/>
						<ContactForm/>
						</>
					}
				</main>
			</Layout>
		</>
	);
}
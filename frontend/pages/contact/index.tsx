import Layout from "@/components/Layout";
import {ContactForm} from "@/components/contact/ContactForm";


export default function Contact() {

	return (
		<>
			<Layout>
				<main>
					{
						<ContactForm/>
					}
				</main>
			</Layout>
		</>
	);
}
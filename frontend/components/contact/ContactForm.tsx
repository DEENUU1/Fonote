import {Button, Input, Textarea} from "@nextui-org/react";
import React, {useState} from "react";
import {toast} from "react-toastify";

export function ContactForm() {
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [email, setEmail] = useState<string>("");
  const [subject, setSubject] = useState<string>("");
  const [message, setMessage] = useState<string>("");
	const [name, setName] = useState<string>("");

  const handleSubmit = async (e: any) => {
    e.preventDefault();

    setIsLoading(true);

    const formData = new FormData();
    formData.append("email", email);
    formData.append("subject", subject);
    formData.append("message", message);
		formData.append("name", name);

    try {
      const response = await fetch(process.env.API_URL + "contact/", {
        method: "POST",
        headers: {
          accept: "application/json",
        },
        body: formData,
      });

      if (response.ok) {
        toast.success("Form submitted successfully");
      } else {
        toast.error("Form submission failed");
      }
    } catch (error) {
      toast.error("Form submission failed");
    } finally {
      setIsLoading(false)
    }
  };

	return (
		<>
			<div className=" my-6 mx-auto max-w-xl">
				<form className="mt-8 space-y-4" onSubmit={handleSubmit}>
					<Input disabled={isLoading} isRequired={true} variant={"faded"} type='text' label={"Name"}
								 placeholder='John Doe' onChange={(e) => setName(e.target.value)}/>
					<Input disabled={isLoading} isRequired={true} variant={"faded"} type='email' label={"Email"}
								 placeholder='Email' onChange={(e) => setEmail(e.target.value)} />
					<Input disabled={isLoading} isRequired={true} variant={"faded"} type='text' label={"Subject"}
								 placeholder='Subject'onChange={(e) => setSubject(e.target.value)}/>
					<Textarea disabled={isLoading} isRequired={true} variant={"faded"} label={"Message"}
										placeholder='Message' onChange={(e) => setMessage(e.target.value)}></Textarea>
					<Button isLoading={isLoading} type='submit'
									className="text-white bg-blue-500 hover:bg-blue-600 font-semibold rounded-md text-sm px-4 py-3 w-full">{isLoading ? 'Sending...' : 'Send'}
					</Button>
				</form>
			</div>
		</>
	)
}
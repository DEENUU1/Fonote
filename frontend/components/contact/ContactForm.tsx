import {Button, Input, Textarea} from "@nextui-org/react";
import React, {useState} from "react";
import {toast} from "react-toastify";

export function ContactForm() {
  const [isLoading, setIsLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    subject: "",
    message: "",
  });

  const handleChange = (e: any) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = async (e: any) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch(`${process.env.API_URL}contact/`, {
        method: "POST",
        headers: {
          accept: "application/json",
        },
        body: new FormData(e.target),
      });

      if (response.ok) {
        toast.success("Form submitted successfully");
      } else {
        toast.error("Form submission failed");
      }
    } catch (error) {
      toast.error("Form submission failed");
    } finally {
      setIsLoading(false);
    }
  };

	return (
    <div className="my-6 mx-auto max-w-xl">
      <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
        <Input
          disabled={isLoading}
          isRequired={true}
          variant={"faded"}
          type="text"
          name="name"
          label={"Name"}
          placeholder="John Doe"
          value={formData.name}
          onChange={handleChange}
        />
        <Input
          disabled={isLoading}
          isRequired={true}
          variant={"faded"}
          type="email"
          name="email"
          label={"Email"}
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
        />
        <Input
          disabled={isLoading}
          isRequired={true}
          variant={"faded"}
          type="text"
          name="subject"
          label={"Subject"}
          placeholder="Subject"
          value={formData.subject}
          onChange={handleChange}
        />
        <Textarea
          disabled={isLoading}
          isRequired={true}
          variant={"faded"}
          name="message"
          label={"Message"}
          placeholder="Message"
          value={formData.message}
          onChange={handleChange}
        ></Textarea>
        <Button
          isLoading={isLoading}
          type="submit"
          className="text-white bg-blue-500 hover:bg-blue-600 font-semibold rounded-md text-sm px-4 py-3 w-full"
        >
          {isLoading ? "Sending..." : "Send"}
        </Button>
      </form>
    </div>
  );
}
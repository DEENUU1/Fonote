import Layout from "@/components/Layout";
import {useSession} from "next-auth/react";
import {useEffect, useState} from "react";
import Link from "next/link";
import ChipStatus from "@/components/dashboard/StatusChip";
import {Chip} from "@nextui-org/react";
import {Modal, ModalContent, ModalHeader, ModalBody, ModalFooter, Button, useDisclosure} from "@nextui-org/react";
import {Input, Select, SelectItem} from "@nextui-org/react";
import {toast} from "react-toastify";
import {Spinner} from "@chakra-ui/react";

async function getListInputData(access_token: string) {
	const res = await fetch(process.env.API_URL + "ai/input/", {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}


async function getInputDataDetails(access_token: string, inputDataId: string){
	const res = await fetch(process.env.API_URL + "ai/input/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}

async function getListResult(access_token: string, inputDataId: string){
	const res = await fetch(process.env.API_URL + "ai/result/" + inputDataId, {
		method: "get",
		headers: {
			Authorization: `Bearer ${access_token}`
		}
	})
	return await res.json()
}


async function postResponse(access_token: string, inputDataId: string, result_type: string){
	const res = await fetch(process.env.API_URL + "ai/result/", {
		method: "post",
		headers: {
			Authorization: `Bearer ${access_token}`,
		 'Content-Type': 'application/json',
			'Accept': 'application/json'
		},
		body: JSON.stringify({
			input_id: inputDataId,
			result_type: result_type
		})
	})
	return await res.json();
}


const resultType: String[] = ["NOTE", "SUMMARY", "BULLETS", "LONG SUMMARY", "LONG NOTE"];
const languages = [
	{label: "English", value: "English", description: "English"},
	{label: "French", value: "French", description: "French"},
	{label: "German", value: "German", description: "German"},
	{label: "Italian", value: "Italian", description: "Italian"},
	{label: "Spanish", value: "Spanish", description: "Spanish"},
	{label: "Japanese", value: "Japanese", description: "Japanese"},
	{label: "Korean", value: "Korean", description: "Korean"},
	{label: "Danish", value: "Danish", description: "Danish"},
	{label: "Czech", value: "Czech", description: "Czech"},
	{label: "Dutch", value: "Dutch", description: "Dutch"},
	{label: "Polish", value: "Polish", description: "Polish"},
]


export default function Dashboard() {
	const {data: session, status} = useSession({required: true});

	const {isOpen, onOpen, onOpenChange} = useDisclosure();
	const [listInputData, setListInputData] = useState([]);
	const [detailInputData, setDetailInputData] = useState(null);
	const [listResult, setListResult] = useState([]);
	const [isLoading, setIsLoading] = useState(false);
	const [url, setUrl] = useState("");
	const [language, setLanguage] = useState("");

	const handleSubmitCreateInputData = async (e: any) => {
    e.preventDefault();

    setIsLoading(true);

    const formData = new FormData();
    formData.append("source_url", url);
    formData.append("language", language);

    try {
      const response = await fetch(process.env.API_URL + "ai/input/", {
        method: "POST",
        headers: {
          accept: "application/json",
					Authorization: `Bearer ${session?.access_token}`
        },
        body: formData,
      });

      if (response.ok) {
        toast.success("Input data created successfully");
      } else {
        toast.error("Error while creating Input data object")
      }
    } catch (error) {
      toast.error("Error while creating Input data object");
    } finally {
      setIsLoading(false)
    }
  };

	useEffect(() => {
		async function fetchData() {
			const data = await getListInputData(session?.access_token);
			setListInputData(data);
		}

		fetchData();
	}, [session?.access_token]);

	const handleListItemClick = async (inputDataId) => {
    const detailInputData = await getInputDataDetails(session?.access_token, inputDataId);
		setDetailInputData(detailInputData);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);
  };

	const handleResponseCreate = async (inputDataId, resultType) => {
		if (!detailInputData){
			toast.error("Input data not found");
			return;
		}


		setIsLoading(true);
		const response = await postResponse(session?.access_token, inputDataId, resultType);

		const listResult = await getListResult(session?.access_token, inputDataId);
		setListResult(listResult);

		setIsLoading(false);
	}

	if (status == "loading") {
    return <Spinner size="lg"/>;
  }

	if (session) {
		return (
			<>
				<Layout>
					<main className={"h-screen"}>
						{
							<>
								<button data-drawer-target="default-sidebar" data-drawer-toggle="default-sidebar"
												aria-controls="default-sidebar" type="button"
												className="inline-flex items-center p-2 mt-2 ms-3 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600">
									<span className="sr-only">Open sidebar</span>
									<svg className="w-6 h-6" aria-hidden="true" fill="currentColor" viewBox="0 0 20 20"
											 xmlns="http://www.w3.org/2000/svg">
										<path clipRule="evenodd" fillRule="evenodd"
													d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"></path>
									</svg>
								</button>

								<aside id="default-sidebar"
											 className="fixed top-0 left-0 z-40 w-64 h-screen transition-transform -translate-x-full sm:translate-x-0"
											 aria-label="Sidebar">
									<div className="h-full px-3 py-4 overflow-y-auto bg-gray-50 dark:bg-gray-800">
										<ul className="space-y-2 font-medium">

											<Button onPress={onOpen}>
												<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth="1.5"
														 stroke="currentColor" className="w-6 h-6">
													<path strokeLinecap="round" strokeLinejoin="round" d="M12 4.5v15m7.5-7.5h-15"/>
												</svg>
											</Button>
											<Modal backdrop={"blur"} isOpen={isOpen} onOpenChange={onOpenChange} isDismissable={false}
														 isKeyboardDismissDisabled={true}>
												<ModalContent>
													{(onClose) => (
														<>
															<ModalHeader className="flex flex-col gap-1">Process data</ModalHeader>
															<form onSubmit={handleSubmitCreateInputData}>
																<ModalBody>
																	<div className={"flex w-full flex-wrap md:flex-nowrap mb-6 md:mb-0 gap-2"}>
																		<Input isRequired={true} type="url" label="Url" placeholder="Youtube/Spotify url"
																					 onChange={(e) => setUrl(e.target.value)}/>
																		<Select
																			isRequired={true}
																			items={languages}
																			label="Langugae"
																			placeholder="Select a language"
																			onChange={(e) => setLanguage(e.target.value)}
																			className="max-w-xs"
																		>
																			{(language) => <SelectItem key={language.value}>{language.label}</SelectItem>}
																		</Select>
																	</div>

																</ModalBody>
																<ModalFooter>
																	<Button color="danger" variant="light" onPress={onClose}>
																		Close
																	</Button>
																	<Button type={"submit"} color="primary" onPress={onClose}>
																		Submit
																	</Button>
																</ModalFooter>
															</form>
														</>
													)}
												</ModalContent>
											</Modal>

											{Array.isArray(listInputData) && (
												listInputData.map((inputData) => (
													<li className={"hover:bg-gray-200 rounded-xl p-2 overflow-hidden overflow-ellipsis"}
															key={inputData?.id}>
														<Link href="#" onClick={() => handleListItemClick(inputData?.id)}>
															<div>
																<span className="flex-1 truncate">{inputData?.source_title}</span>
																<ChipStatus status={inputData?.status}/>
															</div>
														</Link>
													</li>
												))
											)}

										</ul>
									</div>
								</aside>

								<div className="p-4 sm:ml-64 flex flex-wrap h-[850px]">
									<>
										{detailInputData?.fragments.length > 0 && (
											<div className="w-full flex mb-4 gap-2">
												<Chip color={"default"}
															variant={"bordered"}>{detailInputData?.audio_length_minutes} minutes</Chip>
												<Chip color={"default"} variant={"bordered"}>{detailInputData?.language}</Chip>
												<Chip color={"default"} variant={"bordered"}>{detailInputData?.source}</Chip>
												<Chip color={"default"} variant={"bordered"}>{detailInputData?.transcription_type}</Chip>
											</div>
										)
										}
									</>

									<div
										className="p-4 w-1/2 border-2 flex-grow border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
										style={{maxHeight: "850px"}}>
										{detailInputData?.fragments.length > 0 && (
											detailInputData?.fragments.map((detail) => (
												<li key={detail?.id} className={"mb-5 list-none"}>
													<div>
														<Chip color={"default"} variant={"bordered"}>
															<strong>
																{detail.start_time.hours}:{detail.start_time.minutes}:{detail.start_time.seconds}
															</strong>
															-
															<strong>
																{detail.end_time.hours}:{detail.end_time.minutes}:{detail.end_time.seconds}
															</strong>
														</Chip>
														<p>{detail?.text}</p>
													</div>
												</li>
											))
										)}
									</div>
									<div
										className="p-4 w-1/2 border-2 flex-grow border-gray-200 border-solid rounded-lg dark:border-gray-700 overflow-y-auto"
										style={{maxHeight: "850px"}}>
										{Array.isArray(listResult) && (listResult.length > 0 && (
											listResult?.map((result) => (
												<li key={result?.id} className={"mb-5 list-none"}>
													<div>
														<Chip color={"default"} variant={"bordered"}>{result?.result_type}</Chip>
														<p>{result?.content}</p>
													</div>
												</li>
											))
										))}
									</div>

									{resultType.map((resultType, index) => (
										<div key={index} className={"mt-5 gap-2"}>
											<Button className={"mr-2"} variant={"ghost"} size={"sm"} isLoading={isLoading} type={"button"}
															onClick={() => handleResponseCreate(detailInputData?.id, resultType)}>
												{resultType}
											</Button>
										</div>
									))}
								</div>
							</>
						}
					</main>
				</Layout>
			</>
		);
	}

	return <></>;

}
import {
	Button,
	Input,
	Modal,
	ModalBody,
	ModalContent,
	ModalFooter,
	ModalHeader,
	Select,
	SelectItem,
	useDisclosure
} from "@nextui-org/react";
import {aiTranscriptions, languages} from "@/components/dashboard/const";


export default function CreateInputModal(
	{
		handleSubmitCreateInputData,
		setUrl,
		setLanguage,
		setTranscription
	}:
		{
			handleSubmitCreateInputData: (data: any) => void,
			setUrl: (url: string) => void,
			setLanguage: (language: string) => void,
			setTranscription: (transcription: string) => void
		}
) {
	const {isOpen, onOpen, onOpenChange} = useDisclosure();


	return (


		<>
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
									<div className={"flex flex-col gap-2"}>
										<div className="flex gap-2">
											<div className="w-full">
												<Input isRequired={true} type="url" label="Url"
															 placeholder="Youtube/Spotify url"
															 onChange={(e) => setUrl(e.target.value)}/>
											</div>
										</div>
										<div className="flex gap-2">
											<div className="w-full">
												<Select
													isRequired={true}
													items={languages}
													label="Language"
													placeholder="Select a language"
													onChange={(e) => setLanguage(e.target.value)}
												>
													{(language) => <SelectItem key={language.value}>{language.label}</SelectItem>}
												</Select>
											</div>
											<div className="w-full">
												<Select
													isRequired={true}
													items={aiTranscriptions}
													label="Transcription type"
													placeholder="Select a transcription type"
													onChange={(e) => setTranscription(e.target.value)}
												>
													{(transcript) => <SelectItem
														key={transcript.value}>{transcript.label}</SelectItem>}
												</Select>
											</div>
										</div>
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
		</>
	)
}
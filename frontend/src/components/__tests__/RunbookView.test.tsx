import { render, screen } from '@testing-library/react'
import RunbookView from '../RunbookView'

test('renders no query message', ()=>{
  render(<RunbookView query="" />)
  expect(screen.getByText(/No runbook query/i)).toBeTruthy()
})
